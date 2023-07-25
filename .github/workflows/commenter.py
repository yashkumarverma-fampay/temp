name: Pull Request File Changes Comment
on:
  pull_request:
    types:
      - opened

jobs:
  file_changes_comment:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Get edited files
        id: file_changes
        run: echo ::set-output name=files::$(git diff --name-only ${{ github.event.pull_request.base.sha }} ${{ github.event.pull_request.head.sha }})

      - name: Comment on pull request
        uses: actions/github-script@v3
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const files = "${{ steps.file_changes.outputs.files }}".split("\n").filter(Boolean);
            const filesList = files.map(file => `- ${file}`).join("\n");
            const commentBody = `Files edited in this pull request:\n\n${filesList}`;
            github.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: commentBody
            });
