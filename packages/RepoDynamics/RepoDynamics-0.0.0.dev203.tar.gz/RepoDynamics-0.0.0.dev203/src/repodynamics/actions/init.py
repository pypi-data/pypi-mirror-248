import github_contexts
from github_contexts.github.enums import EventType

from repodynamics.logger import Logger
from repodynamics.actions.events.issue_comment import IssueCommentEventHandler
from repodynamics.actions.events.issues import IssuesEventHandler
from repodynamics.actions.events.pull_request import PullRequestEventHandler
from repodynamics.actions.events.pull_request_target import PullRequestTargetEventHandler
from repodynamics.actions.events.push import PushEventHandler
from repodynamics.actions.events.schedule import ScheduleEventHandler
from repodynamics.actions.events.workflow_dispatch import WorkflowDispatchEventHandler
from repodynamics.datatype import TemplateType

# class Init:
#
#     def __init__(
#         self,
#         context: dict,
#         admin_token: str,
#         logger: Logger | None = None,
#     ):
#         self.state: StateManager | None = None
#         self.metadata_branch: dict = {}
#         self.metadata_branch_before: dict = {}
#         self.changed_files: dict[RepoFileType, list[str]] = {}
#         return
#
#     def categorize_labels(self, label_names: list[str]):
#         label_dict = {
#             label_data["name"]: label_key
#             for label_key, label_data in self.metadata_main["label"]["compiled"].items()
#         }
#         out = {}
#         for label in label_names:
#             out[label] = label_dict[label]
#         return out


def init(
    template: str,
    context: dict,
    path_root_self: str,
    path_root_fork: str = "",
    admin_token: str = "",
    package_build: bool = False,
    package_lint: bool = False,
    package_test: bool = False,
    website_build: bool = False,
    meta_sync: str = "none",
    hooks: str = "none",
    website_announcement: str = "",
    website_announcement_msg: str = "",
    logger=None,
):
    try:
        template_type = TemplateType(template)
    except ValueError:
        supported_templates = ", ".join([f"'{enum.value}'" for enum in TemplateType])
        logger.error(
            "Invalid input: template",
            f"Expected one of {supported_templates}; got '{template}' instead.",
        )
        return
    context_manager = github_contexts.context_github(context=context)
    args = {
        "template_type": template_type,
        "context_manager": context_manager,
        "path_root_self": path_root_self,
        "path_root_fork": path_root_fork,
        "admin_token": admin_token,
        "logger": logger
    }
    event = context_manager.github.event_name
    if event is EventType.ISSUES:
        event_manager = IssuesEventHandler(**args)
    elif event is EventType.ISSUE_COMMENT:
        event_manager = IssueCommentEventHandler(**args)
    elif event is EventType.PULL_REQUEST:
        event_manager = PullRequestEventHandler(**args)
    elif event is EventType.PULL_REQUEST_TARGET:
        event_manager = PullRequestTargetEventHandler(**args)
    elif event is EventType.PUSH:
        event_manager = PushEventHandler(**args)
    elif event is EventType.SCHEDULE:
        event_manager = ScheduleEventHandler(**args)
    elif event is EventType.WORKFLOW_DISPATCH:
        event_manager = WorkflowDispatchEventHandler(
            package_build=package_build,
            package_lint=package_lint,
            package_test=package_test,
            website_build=website_build,
            meta_sync=meta_sync,
            hooks=hooks,
            website_announcement=website_announcement,
            website_announcement_msg=website_announcement_msg,
            **args,
        )
    else:
        logger.error(f"Event '{event}' is not supported.")
    return event_manager.run()
