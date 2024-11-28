# code-stingray

code-stingray is a lightweight CLI that leverages GenAI for code review, seamlessly integrating with both GenAI models and CI/CD tools.

## Prerequisites
### Google
Please make sure you already [set up a project and a development environment of VertexAI](https://cloud.google.com/vertex-ai/docs/start/cloud-environment). You can use available [Gemini models](https://ai.google.dev/gemini-api/docs/models/gemini) as the LLM for this project. 

Please refer to [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation) or [set up Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc) when you are on your laptop or any other environment outside GCP.

<!-- ## Architecture
```plantuml
@startuml
!include <C4/C4_Container>


title Container diagram of Code Stingray
LAYOUT_WITH_LEGEND()


Person(user, "User", "A developer enabled by GenAI code review")
Container_Ext(git_platform, "Git Platform", "GitHub", "Collaborative Git platform to host your awesome code")
System_Boundary(gcp, "GCP") {
    Container(cloudbuild, "CI/CD", "Cloud Build", "A native serverless CI/CD platform in GCP")
    Container(secret_provider, "Secret Manager", "Secret Manager", "Store API keys, passwords, certificates, and sensitive data")
    Container(genai, "Code Stingray", "Gemini", "Review the modified code in the pull request")
}

Rel(user, git_platform, "Raise a Pull  Request ", "Bitbucket UI")
Rel(git_platform, cloudbuild, "Trigger", "Cloud Build Trigger")
Rel(cloudbuild, secret_provider, "Fetch secrets", "")
Rel(cloudbuild, genai, "Raise a container", "")
Rel(genai, git_platform, "Post review result", "GitPython")

@enduml

``` -->


## Development
### Export requirements
```bash
poetry export -f requirements.txt --without-hashes --output requirements.txt
```

### Version Bump
```bash
bump2version major  # Bump major version
bump2version minor  # Bump minor version
bump2version patch  # Bump patch version 
```

## License and Attribution
This project includes material from [genai-for-developers](https://github.com/GoogleCloudPlatform/genai-for-developers), licensed under the Apache License, Version 2.0. 
You can view the full license at http://www.apache.org/licenses/LICENSE-2.0