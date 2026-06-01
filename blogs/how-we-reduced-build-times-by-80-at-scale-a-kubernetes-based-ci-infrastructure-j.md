# How We Reduced Build Times by 80% at Scale: A Kubernetes-Based CI Infrastructure

Last year, our engineering team spent more time waiting for builds than writing code. With 45-minute average build times and a queue that regularly backed up to 200+ jobs, our CI infrastructure had become the bottleneck killing our velocity. Six months later, we've cut those build times to under 9 minutes. Here's exactly how we did it.

## The Breaking Point

When you're shipping 50+ deployments per day across 12 microservices with 80 engineers, CI infrastructure isn't just a convenience. It's critical path. Our breaking point came during a production incident when a hotfix sat in the build queue for 23 minutes before even starting. That's when we knew our legacy Jenkins setup couldn't scale with us anymore.

## Understanding Our Legacy Bottlenecks

Our old infrastructure ran on a fleet of 15 static Jenkins agents on EC2. The problems were predictable:

- **Fixed capacity**: We paid for peak load 24/7, yet still hit queuing during busy hours
- **Snowflake configurations**: Each agent had accumulated years of drift
- **No isolation**: Builds competed for resources and occasionally corrupted each other's state
- **Slow feedback loops**: Developers context-switched while waiting, destroying productivity

Profiling our builds revealed that only 40% of wall-clock time was actual compilation. The rest? Dependency downloads, Docker layer rebuilds, and queue wait time.

## Why We Chose Kubernetes for CI

We evaluated GitHub Actions, CircleCI, BuildKite, and Kubernetes-native options. Our decision matrix prioritized:

1. **Cost efficiency at scale**: We needed elastic scaling without premium SaaS pricing
2. **Customization**: Our monorepo required specific tooling (and choosing the right build system for monorepos matters. See our comparison of [Bazel vs Gradle vs Nx](/blog/bazel-vs-gradle-vs-nx-choosing-the-right-build-system-for-monorepos-in-2024))
3. **Existing expertise**: Our team already operated production Kubernetes clusters

We chose a **Kubernetes-based CI infrastructure** using Tekton for pipeline orchestration. The ability to use our existing cluster expertise, combined with true elastic scaling and complete control over the build environment, made this the clear winner.

## Architecture Deep Dive

Our Kubernetes build pipeline architecture centers on three core components. This work became a foundational piece of [building a developer platform from CI/CD pipelines to internal developer portals](/blog/building-a-developer-platform-from-ci-cd-pipelines-to-internal-developer-portals):

```yaml
# Simplified Tekton Pipeline structure
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: microservice-build
spec:
  workspaces:
    - name: shared-workspace
    - name: cache-workspace
  tasks:
    - name: fetch-source
      taskRef:
        name: git-clone
    - name: run-tests
      taskRef:
        name: parallel-test-runner
      runAfter: ["fetch-source"]
    - name: build-image
      taskRef:
        name: kaniko-build
      runAfter: ["run-tests"]
```

**Key architectural decisions:**

- **Ephemeral build pods**: Every build gets a fresh environment, eliminating state drift. We also implemented [feature flags infrastructure that scales](/blog/how-to-design-and-implement-feature-flags-infrastructure-that-scales) to gradually roll out new build configurations without disrupting developer workflows.