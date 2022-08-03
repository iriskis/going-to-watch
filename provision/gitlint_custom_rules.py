import re

from gitlint.rules import CommitRule, RuleViolation


class BranchName(CommitRule):
    """Rule to validate branch name."""
    name = "branch-name"
    id = "UC1"

    def validate(self, commit):
        """Validate branch name."""
        branch_name_format = (
            r"^(feature|hotfix)\/PYCAMP-\d+(?:-[a-z]+)+$"
        )

        if re.fullmatch(branch_name_format, commit.context.current_branch):
            return None

        msg = (
            "Branch name does not valid. "
            "Template: feature/[task-id]-[short-and-meaningful-description]"
        )
        return [RuleViolation(self.id, msg, line_nr=1)]
