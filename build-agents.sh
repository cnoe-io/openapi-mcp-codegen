#!/bin/bash

# Build multi-arch containers for Argo services
# Usage: ./build-agents.sh [--push] [service-name]

set -euo pipefail

# Configuration
REGISTRY="ghcr.io/cnoe-io"
DATE_TAG=$(date +%Y%m%d-%H%M%S)
AUTOGEN_TAG="autogen-${DATE_TAG}"
PLATFORMS="linux/amd64,linux/arm64"

# Parse arguments
PUSH_FLAG=""
SINGLE_SERVICE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --push)
            PUSH_FLAG="--push"
            shift
            ;;
        argo-workflows|argocd|argo-rollouts)
            SINGLE_SERVICE="$1"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--push] [argo-workflows|argocd|argo-rollouts]"
            exit 1
            ;;
    esac
done

if [[ -n "${PUSH_FLAG}" ]]; then
    echo "🚀 Push mode enabled - images will be pushed to registry"
else
    echo "🏗️  Build mode - images will be built locally only"
    echo "   Use '--push' to push to registry"
fi

if [[ -n "${SINGLE_SERVICE}" ]]; then
    echo "🎯 Single service mode - building only: ${SINGLE_SERVICE}"
fi

# Services configuration - using arrays for bash 3.x compatibility
SERVICES_KEYS=("argo-workflows" "argocd" "argo-rollouts")
SERVICES_VALUES=("agent-argo-workflows" "agent-argocd" "agent-argo-rollouts")

# Function to get service image name by key
get_service_image() {
    local key="$1"
    for i in "${!SERVICES_KEYS[@]}"; do
        if [[ "${SERVICES_KEYS[$i]}" == "$key" ]]; then
            echo "${SERVICES_VALUES[$i]}"
            return 0
        fi
    done
    return 1
}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi

    if ! docker buildx version &> /dev/null; then
        log_error "Docker buildx is not available"
        exit 1
    fi

    # Create buildx builder for multi-arch if it doesn't exist
    if ! docker buildx inspect multiarch-builder &> /dev/null; then
        log_info "Creating multi-arch builder..."
        docker buildx create --name multiarch-builder --driver docker-container --platform ${PLATFORMS}
        docker buildx use multiarch-builder
    else
        docker buildx use multiarch-builder
    fi

    log_success "Prerequisites check passed"
}

# Build function for both MCP and A2A variants
build_service() {
    local service_name=$1
    local image_name=$2
    local dockerfile_type=$3  # "mcp" or "a2a"

    log_info "Building ${dockerfile_type^^} variant for ${service_name}..."

    # Check if generate_code directory exists
    if [[ ! -d "examples/${service_name}/generate_code" ]]; then
        log_error "Generated code not found for ${service_name}. Run 'make generate-${service_name}-agent' first."
        return 1
    fi

    local dockerfile="build/Dockerfile.${dockerfile_type}.agent"
    local full_image_name="${REGISTRY}/${image_name}-${dockerfile_type}"

    # Build arguments
    local build_args=(
        "--platform" "${PLATFORMS}"
        "--build-arg" "SERVICE_NAME=${service_name}"
        "-f" "${dockerfile}"
        "-t" "${full_image_name}:${AUTOGEN_TAG}"
        "-t" "${full_image_name}:latest"
        "."
    )

    if [[ -n "${PUSH_FLAG}" ]]; then
        build_args+=("${PUSH_FLAG}")
    fi

    # Execute build
    if docker buildx build "${build_args[@]}"; then
        log_success "Built ${full_image_name}:${AUTOGEN_TAG}"
        if [[ -n "${PUSH_FLAG}" ]]; then
            log_success "Pushed ${full_image_name}:${AUTOGEN_TAG}"
        fi
    else
        log_error "Failed to build ${full_image_name}"
        return 1
    fi
}

# Main build process
main() {
    log_info "Starting multi-arch build for Argo services"
    log_info "Date tag: ${DATE_TAG}"
    log_info "Autogen tag: ${AUTOGEN_TAG}"
    log_info "Registry: ${REGISTRY}"
    log_info "Platforms: ${PLATFORMS}"
    echo

    check_prerequisites
    echo

    # Build services (all or single)
    local failed_builds=()
    local services_to_build=()

    if [[ -n "${SINGLE_SERVICE}" ]]; then
        # Validate single service exists in SERVICES array
        if ! get_service_image "${SINGLE_SERVICE}" > /dev/null; then
            log_error "Unknown service: ${SINGLE_SERVICE}"
            log_info "Available services: ${SERVICES_KEYS[*]}"
            exit 1
        fi
        services_to_build=("${SINGLE_SERVICE}")
    else
        services_to_build=("${SERVICES_KEYS[@]}")
    fi
    
    # Check if we have services to build
    if [[ ${#services_to_build[@]} -eq 0 ]]; then
        log_error "No services to build"
        exit 1
    fi
    
    for service_name in "${services_to_build[@]}"; do
        image_name=$(get_service_image "${service_name}")

        echo "=================================================="
        log_info "Processing ${service_name} -> ${image_name}"
        echo "=================================================="

        # Build MCP variant
        if build_service "${service_name}" "${image_name}" "mcp"; then
            log_success "MCP build completed for ${service_name}"
        else
            failed_builds+=("${service_name}-mcp")
        fi

        echo

        # Build A2A variant
        if build_service "${service_name}" "${image_name}" "a2a"; then
            log_success "A2A build completed for ${service_name}"
        else
            failed_builds+=("${service_name}-a2a")
        fi

        echo
    done

    # Summary
    echo "=================================================="
    log_info "BUILD SUMMARY"
    echo "=================================================="

    if [[ ${#failed_builds[@]} -eq 0 ]]; then
        log_success "All builds completed successfully! 🎉"
        echo
        log_info "Built images:"
        for service_name in "${services_to_build[@]}"; do
            image_name=$(get_service_image "${service_name}")
            echo "  📦 ${REGISTRY}/${image_name}-mcp:${AUTOGEN_TAG}"
            echo "  📦 ${REGISTRY}/${image_name}-a2a:${AUTOGEN_TAG}"
        done
    else
        log_error "Some builds failed:"
        for failed in "${failed_builds[@]}"; do
            echo "  ❌ ${failed}"
        done
        exit 1
    fi

    if [[ -z "${PUSH_FLAG}" ]]; then
        echo
        log_warning "Images built locally only. Use '--push' to push to registry."
        log_info "To push manually:"
        for service_name in "${services_to_build[@]}"; do
            image_name=$(get_service_image "${service_name}")
            echo "  docker push ${REGISTRY}/${image_name}-mcp:${AUTOGEN_TAG}"
            echo "  docker push ${REGISTRY}/${image_name}-a2a:${AUTOGEN_TAG}"
        done
    fi
}

# Run main function
main "$@"
