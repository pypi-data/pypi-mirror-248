from __future__ import annotations

import copy
import os
import subprocess

from git import Repo

from argrelay.custom_integ.GitRepoArgType import GitRepoArgType
from argrelay.custom_integ.GitRepoDelegator import repo_root_abs_path_
from argrelay.custom_integ.GitRepoEntryConfigSchema import (
    repo_rel_path_,
    envelope_properties_,
    is_repo_enabled_,
)
from argrelay.custom_integ.GitRepoEnvelopeClass import GitRepoEnvelopeClass
from argrelay.custom_integ.GitRepoLoaderConfigSchema import (
    git_repo_loader_config_desc,
    load_repo_commits_,
    repo_entries_,
)
from argrelay.enum_desc.ReservedArgType import ReservedArgType
from argrelay.misc_helper import eprint
from argrelay.plugin_loader.AbstractLoader import AbstractLoader
from argrelay.runtime_data.StaticData import StaticData
from argrelay.schema_config_interp.DataEnvelopeSchema import (
    envelope_id_,
    envelope_payload_,
)


class GitRepoLoader(AbstractLoader):
    """
    Implements FS_67_16_61_97 git_plugin.
    """

    def __init__(
        self,
        plugin_instance_id: str,
        config_dict: dict,
    ):
        super().__init__(
            plugin_instance_id,
            config_dict,
        )
        self.config_dict = git_repo_loader_config_desc.from_input_dict(self.config_dict)

    def validate_config(
        self,
    ):
        git_repo_loader_config_desc.validate_dict(self.config_dict)

    def update_static_data(
        self,
        static_data: StaticData,
    ) -> StaticData:
        """
        Scan `base_path` recursively and load metadata about all Git repos found.
        """

        if not self.config_dict:
            return static_data

        static_data = self.load_git_objects(static_data)

        return static_data

    def load_git_objects(
        self,
        static_data: StaticData,
    ) -> StaticData:

        data_envelopes = static_data.data_envelopes

        # Init type keys (if they do not exist):
        for type_name in [enum_item.name for enum_item in GitRepoArgType]:
            if type_name not in static_data.known_arg_types:
                static_data.known_arg_types.append(type_name)

        # List of registered Git abs paths:
        repo_root_abs_paths = []
        for repo_base_abs_path in self.config_dict[repo_entries_]:

            repo_entries = self.config_dict[repo_entries_][repo_base_abs_path]
            repo_base_abs_path = os.path.expanduser(repo_base_abs_path)

            # Process repo entries collecting `repo_root_rel_path` and `repo_root_abs_path`:
            for repo_entry in repo_entries:

                repo_root_rel_path = repo_entry[repo_rel_path_]
                repo_root_abs_path = os.path.join(repo_base_abs_path, repo_root_rel_path)

                if not repo_entry[is_repo_enabled_]:
                    eprint(f"INFO: disabled repo: {repo_root_abs_path}")
                    continue

                # Deduplicate Git root paths:
                if repo_root_abs_path not in repo_root_abs_paths:
                    # Register `repo_root_abs_path`:
                    repo_root_abs_paths.append(repo_root_abs_path)
                else:
                    eprint(f"ERROR: duplicate Git repo: {repo_root_abs_path}")
                    raise RuntimeError

                # Query Git root path of curr dir:
                subproc = subprocess.run(
                    [
                        "git",
                        "-C",
                        repo_root_abs_path,
                        "rev-parse",
                        "--show-toplevel",
                    ],
                    capture_output = True,
                )
                ret_code = subproc.returncode

                if ret_code == 0:
                    pass
                else:
                    eprint(f"ERROR: not a Git repo: {repo_root_abs_path}")
                    # Walked into dir outside of Git repo:
                    continue

                repo_root_base_name = os.path.basename(repo_root_abs_path)

                # Produce path component list, for example, if:
                # repo_root_rel_path = "rel/path/to/git/repo.git/"
                # then:
                # path_comp_list = [ "rel", "path", "to", "git", "repo" ]
                path_comp_list = []
                for rel_git_path_comp in repo_root_rel_path.split(os.sep)[:-1]:
                    if rel_git_path_comp not in path_comp_list:
                        path_comp_list.append(rel_git_path_comp)

                ############################################################################################################
                # repos

                repo_envelope: dict = copy.deepcopy(repo_entry[envelope_properties_])

                repo_envelope.update({
                    envelope_id_: repo_root_abs_path,
                    envelope_payload_: {
                        repo_root_abs_path_: repo_root_abs_path,
                    },
                    ReservedArgType.EnvelopeClass.name: GitRepoEnvelopeClass.ClassGitRepo.name,
                    GitRepoArgType.GitRepoRootRelPath.name: repo_root_rel_path,
                    GitRepoArgType.GitRepoRootAbsPath.name: repo_root_abs_path,
                    GitRepoArgType.GitRepoRootBaseName.name: repo_root_base_name,
                    GitRepoArgType.GitRepoPathComp.name: path_comp_list,
                })
                print(repo_envelope)
                data_envelopes.append(repo_envelope)

                if not self.config_dict[load_repo_commits_]:
                    continue

                git_repo = Repo(repo_root_abs_path)
                for git_commit in git_repo.iter_commits():
                    ########################################################################################################
                    # commits

                    commit_envelope: dict = copy.deepcopy(repo_entry[envelope_properties_])

                    commit_envelope.update({
                        envelope_id_: f"{repo_root_abs_path}:{git_commit.hexsha}",
                        envelope_payload_: {
                        },
                        ReservedArgType.EnvelopeClass.name: GitRepoEnvelopeClass.ClassGitCommit.name,
                        GitRepoArgType.GitRepoRootRelPath.name: repo_root_rel_path,
                        GitRepoArgType.GitRepoRootAbsPath.name: repo_root_abs_path,
                        GitRepoArgType.GitRepoRootBaseName.name: repo_root_base_name,
                        GitRepoArgType.GitRepoPathComp.name: path_comp_list,
                        GitRepoArgType.GitRepoCommitId.name: git_commit.hexsha,
                        GitRepoArgType.GitRepoCommitAuthorName.name: git_commit.author.name,
                        GitRepoArgType.GitRepoCommitAuthorEmail.name: git_commit.author.email,
                        GitRepoArgType.GitRepoCommitMessage.name: git_commit.message,
                    })
                    data_envelopes.append(commit_envelope)

        return static_data
