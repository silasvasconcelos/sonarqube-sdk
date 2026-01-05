from sonarqube import SonarQubeClient

server = "https://sonarqube.hom.dotgroup.com.br"
token = "sqp_aaf7499f08d2343608c1cb25112a3948611f561b"

client = SonarQubeClient(base_url=server, token=token)


projects = client.projects.search(q="dot-group-web")

# issues = client.issues.search(
#     project_keys=["dot-group-web"], severities=["CRITICAL", "BLOCKER"]
# )
# for issue in issues.issues:
#     print(issue.key, issue.message, issue.severity, sep="\t")
#     print("-" * 100)
