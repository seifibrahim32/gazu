from typing import Sequence
import unittest
import json
import requests_mock

import gazu.client
import gazu.shot

from utils import fakeid, mock_route


class ShotTestCase(unittest.TestCase):
    def test_all_shots_for_project(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/projects/project-01/shots"),
                text=json.dumps([{"name": "Shot 01", "project_id": "project-01"}]),
            )
            project = {"id": "project-01"}
            shots = gazu.shot.all_shots_for_project(project)
            self.assertEqual(len(shots), 1)
            shot_instance = shots[0]
            self.assertEqual(shot_instance["name"], "Shot 01")
            self.assertEqual(shot_instance["project_id"], "project-01")

    def test_all_shots_for_sequence(self):
        with requests_mock.mock() as mock:
            mock_route(
                mock,
                "GET",
                "data/sequences/sequence-01/shots",
                text=[
                    {
                        "name": "Shot 01",
                        "project_id": "project-01",
                        "parent_id": "sequence-01",
                    }
                ],
            )
            sequence = {"id": "sequence-01"}
            shots = gazu.shot.all_shots_for_sequence(sequence)
            self.assertEqual(len(shots), 1)
            shot_instance = shots[0]
            self.assertEqual(shot_instance["name"], "Shot 01")
            self.assertEqual(shot_instance["project_id"], "project-01")
            self.assertEqual(shot_instance["parent_id"], "sequence-01")

    def test_all_shots_for_episode(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/episodes/episode-01/shots"),
                text=json.dumps(
                    [
                        {
                            "name": "Shot 01",
                            "project_id": "project-01",
                            "parent_id": "sequence-01",
                        }
                    ]
                ),
            )
            episode = {"id": "episode-01"}
            shots = gazu.shot.all_shots_for_episode(episode)
            self.assertEqual(len(shots), 1)
            shot_instance = shots[0]
            self.assertEqual(shot_instance["name"], "Shot 01")
            self.assertEqual(shot_instance["project_id"], "project-01")
            self.assertEqual(shot_instance["parent_id"], "sequence-01")

    def test_all_sequences_for_project(self):
        with requests_mock.mock() as mock:
            mock_route(
                mock,
                "GET",
                "data/projects/project-01/sequences",
                text=[{"name": "Sequence 01", "project_id": "project-01"}],
            )
            project = {"id": "project-01"}
            sequences = gazu.shot.all_sequences_for_project(project)
            self.assertEqual(len(sequences), 1)
            sequence_instance = sequences[0]
            self.assertEqual(sequence_instance["name"], "Sequence 01")
            self.assertEqual(sequence_instance["project_id"], "project-01")

    def test_all_sequences_for_episode(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/episodes/episode-1/sequences"),
                text=json.dumps(
                    [
                        {
                            "name": "Sequence 01",
                            "project_id": "project-01",
                            "parent_id": "episode-1",
                        }
                    ]
                ),
            )
            episode = {"id": "episode-1"}
            sequences = gazu.shot.all_sequences_for_episode(episode)
            self.assertEqual(len(sequences), 1)
            sequence_instance = sequences[0]
            self.assertEqual(sequence_instance["name"], "Sequence 01")
            self.assertEqual(sequence_instance["project_id"], "project-01")
            self.assertEqual(sequence_instance["parent_id"], "episode-1")

    def test_all_episodes_for_project(self):
        with requests_mock.mock() as mock:
            mock_route(
                mock,
                "GET",
                "data/projects/project-01/episodes",
                text=[{"name": "Episode 01", "project_id": "project-01"}],
            )
            project = {"id": "project-01"}
            episodes = gazu.shot.all_episodes_for_project(project)
            self.assertEqual(len(episodes), 1)
            episode_instance = episodes[0]
            self.assertEqual(episode_instance["name"], "Episode 01")
            self.assertEqual(episode_instance["project_id"], "project-01")

    def test_get_episode(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/episodes/episode-1"),
                text=json.dumps({"name": "Episode 01", "project_id": "project-01"}),
            )
            episode = gazu.shot.get_episode("episode-1")
            self.assertEqual(episode["name"], "Episode 01")

    def test_get_episode_from_sequence(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/episodes/episode-1"),
                text=json.dumps({"name": "Episode 01", "project_id": "project-01"}),
            )
            episode = gazu.shot.get_episode_from_sequence(
                {"id": "shot-01", "parent_id": "episode-1"}
            )
            self.assertEqual(episode["name"], "Episode 01")

    def test_get_sequence(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/sequences/sequence-01"),
                text=json.dumps({"name": "Sequence 01", "project_id": "project-01"}),
            )
            sequence = gazu.shot.get_sequence("sequence-01")
            self.assertEqual(sequence["name"], "Sequence 01")

    def test_get_sequence_from_shot(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/sequences/sequence-01"),
                text=json.dumps({"name": "Sequence 01", "project_id": "project-01"}),
            )
            sequence = gazu.shot.get_sequence_from_shot(
                {"id": "shot-01", "parent_id": "sequence-01"}
            )
            self.assertEqual(sequence["name"], "Sequence 01")

    def test_get_shot(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/shots/shot-01"),
                text=json.dumps({"name": "Shot 01", "project_id": "project-01"}),
            )
            shot = gazu.shot.get_shot("shot-01")
            self.assertEqual(shot["name"], "Shot 01")

    def test_get_shot_by_name(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/shots/all?sequence_id=sequence-01&name=Shot01"
                ),
                text=json.dumps([{"name": "Shot01", "project_id": "project-01"}]),
            )
            sequence = {"id": "sequence-01"}
            shot = gazu.shot.get_shot_by_name(sequence, "Shot01")
            self.assertEqual(shot["name"], "Shot01")

    def test_get_sequence_by_name(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/sequences?project_id=project-01&name=Sequence01"
                ),
                text=json.dumps([{"name": "Sequence01", "project_id": "project-01"}]),
            )
            project = {"id": "project-01"}
            sequence = gazu.shot.get_sequence_by_name(project, "Sequence01")
            self.assertEqual(sequence["name"], "Sequence01")

    def test_new_episode(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/episodes?project_id=project-01&name=Episode 01"
                ),
                text=json.dumps([]),
            )
            mock.post(
                gazu.client.get_full_url("data/projects/project-01/episodes"),
                text=json.dumps({"id": "episode-01", "project_id": "project-01"}),
            )
            project = {"id": "project-01"}
            shot = gazu.shot.new_episode(project, "Episode 01")
            self.assertEqual(shot["id"], "episode-01")

            mock.get(
                gazu.client.get_full_url(
                    "data/episodes?project_id=project-01&name=Episode 01"
                ),
                text=json.dumps([{"id": "episode-01", "project_id": "project-01"}]),
            )

            shot = gazu.shot.new_episode(project, "Episode 01")
            self.assertEqual(shot["id"], "episode-01")

    def test_new_sequence(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/sequences?episode_id=episode-1&name=Sequence 01"
                ),
                text=json.dumps([]),
            )
            mock.post(
                gazu.client.get_full_url("data/projects/project-01/sequences"),
                text=json.dumps({"id": "sequence-01", "project_id": "project-01"}),
            )
            project = {"id": "project-01"}
            episode = {"id": "episode-1"}
            shot = gazu.shot.new_sequence(project, "Sequence 01", episode)
            self.assertEqual(shot["id"], "sequence-01")

            mock.get(
                gazu.client.get_full_url("data/sequences?name=Sequence 01"),
                text=json.dumps([]),
            )
            mock.post(
                gazu.client.get_full_url("data/projects/project-01/sequences"),
                text=json.dumps({"id": "sequence-01", "project_id": "project-01"}),
            )
            project = {"id": "project-01"}
            shot = gazu.shot.new_sequence(project, "Sequence 01")
            self.assertEqual(shot["id"], "sequence-01")

            mock.get(
                gazu.client.get_full_url("data/sequences?name=Sequence 01"),
                text=json.dumps([{"id": "sequence-01", "project_id": "project-01"}]),
            )

            project = {"id": "project-01"}
            shot = gazu.shot.new_sequence(project, "Sequence 01")
            self.assertEqual(shot["id"], "sequence-01")

    def test_new_shot(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/shots/all?sequence_id=sequence-01&name=Shot 01"
                ),
                text=json.dumps([]),
            )
            mock = mock.post(
                gazu.client.get_full_url("data/projects/project-01/shots"),
                text=json.dumps({"id": "shot-01", "project_id": "project-01"}),
            )
            project = {"id": "project-01"}
            sequence = {"id": "sequence-01"}
            shot = gazu.shot.new_shot(
                project, sequence, "Shot 01", nb_frames=10, frame_in=10, frame_out=20
            )
            self.assertEqual(shot["id"], "shot-01")
            sent_data = json.loads(mock.request_history[0].text)
            self.assertEqual(10, sent_data["data"]["frame_in"])

        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/shots/all?sequence_id=sequence-01&name=Shot 01"
                ),
                text=json.dumps([{"id": "shot-01", "project_id": "project-01"}]),
            )

            shot = gazu.shot.new_shot(
                project, sequence, "Shot 01", nb_frames=10, frame_in=10, frame_out=20
            )
            self.assertEqual(shot["id"], "shot-01")

    def test_update_shot(self):
        with requests_mock.mock() as mock:
            mock.put(
                gazu.client.get_full_url("data/entities/shot-01"),
                text=json.dumps({"id": "shot-01", "project_id": "project-01"}),
            )
            shot = {"id": "shot-01", "name": "S02"}
            shot = gazu.shot.update_shot(shot)
            self.assertEqual(shot["id"], "shot-01")

    def test_remove_shot(self):
        with requests_mock.mock() as mock:
            mock.delete(gazu.client.get_full_url("data/shots/shot-01"), status_code=204)
            shot = {"id": "shot-01", "name": "S02"}
            gazu.shot.remove_shot(shot)
            mock.delete(
                gazu.client.get_full_url("data/shots/shot-01?force=true"),
                status_code=204,
            )
            shot = {"id": "shot-01", "name": "S02"}
            gazu.shot.remove_shot(shot, True)

    def test_remove_sequence(self):
        with requests_mock.mock() as mock:
            mock.delete(
                gazu.client.get_full_url("data/sequences/sequence-01?force=true"),
                status_code=204,
            )
            sequence = {"id": "sequence-01", "name": "S02"}
            gazu.shot.remove_sequence(sequence, True)

    def test_remove_episode(self):
        with requests_mock.mock() as mock:
            mock.delete(
                gazu.client.get_full_url("data/episodes/episode-1?force=true"),
                status_code=204,
            )
            episode = {"id": "episode-1", "name": "S02"}
            episode = gazu.shot.remove_episode(episode, True)

    def test_get_asset_instances(self):
        with requests_mock.mock() as mock:
            result = [{"id": "asset-instance-01"}]
            mock.get(
                gazu.client.get_full_url("data/shots/shot-01/asset-instances"),
                text=json.dumps(result),
            )
            shot = {"id": "shot-01"}
            asset_instances = gazu.shot.all_asset_instances_for_shot(shot)
            self.assertEqual(asset_instances[0]["id"], "asset-instance-01")

    def test_add_asset_instance(self):
        with requests_mock.mock() as mock:
            result = {"id": "asset-instance-01"}
            mock.post(
                gazu.client.get_full_url("data/shots/shot-01/asset-instances"),
                text=json.dumps(result),
            )
            shot = {"id": "shot-01"}
            asset_instance = {"id": "asset-instance-1"}
            asset_instance = gazu.shot.add_asset_instance_to_shot(shot, asset_instance)
            self.assertEqual(asset_instance, result)

    def test_remove_asset_instance(self):
        with requests_mock.mock() as mock:
            mock.delete(
                gazu.client.get_full_url(
                    "data/shots/shot-01/asset-instances/asset-instance-1"
                )
            )
            shot = {"id": "shot-01"}
            asset_instance = {"id": "asset-instance-1"}
            asset_instance = gazu.shot.remove_asset_instance_from_shot(
                shot, asset_instance
            )

    def test_get_url(self):
        with requests_mock.mock() as mock:
            shot = {
                "id": "shot-01",
                "project_id": "project-01",
                "episode_id": "episode-01",
            }
            project = {
                "id": "project-01",
                "production_type": "tvshow",
            }
            mock.get(
                gazu.client.get_full_url("data/projects/project-01"),
                text=json.dumps(project),
            )
            mock.get(
                gazu.client.get_full_url("data/shots/%s" % fakeid("shot-01")),
                text=json.dumps(shot),
            )
            url = gazu.shot.get_shot_url(fakeid("shot-01"))
            self.assertEqual(
                url,
                "http://gazu-server/productions/project-01/"
                "episodes/episode-01/shots/shot-01/",
            )

            shot = {"id": "shot-01", "project_id": "project-01", "episode_id": None}
            project = {
                "id": "project-01",
                "production_type": "tvshow",
            }
            mock.get(
                gazu.client.get_full_url("data/projects/project-01"),
                text=json.dumps(project),
            )
            mock.get(
                gazu.client.get_full_url("data/shots/%s" % fakeid("shot-01")),
                text=json.dumps(shot),
            )
            url = gazu.shot.get_shot_url(fakeid("shot-01"))
            self.assertEqual(
                url, "http://gazu-server/productions/project-01/" "shots/shot-01/"
            )

    def test_all_sequences_for_episode(self):
        with requests_mock.mock() as mock:
            mock_route(
                mock,
                "GET",
                "data/episodes/episode-01/sequences",
                text=[{"name": "sequence1", "id": "sequence-01"}],
            )
            episode = {"id": "episode-01"}
            sequences = gazu.shot.all_sequences_for_episode(episode)
            sequence = sequences[0]
            self.assertEqual(len(sequences), 1)
            self.assertEqual(sequence["name"], "sequence1")

    def test_all_previews_for_shot(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/shots/%s/preview-files" % fakeid("shot-1")
                ),
                text=json.dumps(
                    [
                        {"id": fakeid("preview-1"), "name": "preview-1"},
                        {"id": fakeid("preview-2"), "name": "preview-2"},
                    ]
                ),
            )

            previews = gazu.shot.all_previews_for_shot(fakeid("shot-1"))
            self.assertEqual(len(previews), 2)
            self.assertEqual(previews[0]["id"], fakeid("preview-1"))
            self.assertEqual(previews[1]["id"], fakeid("preview-2"))

    def test_get_episode_url(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/episodes/%s" % fakeid("episode-1")),
                text=json.dumps(
                    {
                        "id": fakeid("episode-1"),
                        "project_id": fakeid("project-1"),
                    }
                ),
            )
            url = gazu.shot.get_episode_url(fakeid("episode-1"))
            self.assertEqual(
                url,
                "http://gazu-server/productions/%s/"
                "episodes/%s/shots" % (fakeid("project-1"), fakeid("episode-1")),
            )

    def test_update_sequence(self):
        with requests_mock.mock() as mock:
            mock.put(
                gazu.client.get_full_url("data/entities/%s" % fakeid("sequence-1")),
                text=json.dumps({"id": fakeid("sequence-1"), "name": "sequence-1"}),
            )
            sequence = {"id": fakeid("sequence-1"), "name": "sequence-1"}
            sequence = gazu.shot.update_sequence(sequence)
            self.assertEqual(sequence["name"], "sequence-1")

    def test_get_asset_instances_for_shot(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/shots/%s/asset-instances" % fakeid("shot-1")
                ),
                text=json.dumps(
                    [
                        {"id": fakeid("asset_instance-1"), "name": "asset_instance-1"},
                        {"id": fakeid("asset_instance-2"), "name": "asset_instance-2"},
                    ]
                ),
            )
            asset_instances = gazu.shot.get_asset_instances_for_shot(fakeid("shot-1"))
            self.assertEqual(len(asset_instances), 2)
            self.assertEqual(asset_instances[0]["id"], fakeid("asset_instance-1"))
            self.assertEqual(asset_instances[1]["id"], fakeid("asset_instance-2"))

    def test_update_shot_data(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/shots/%s" % fakeid("shot-1")),
                text=json.dumps({"id": fakeid("shot-1"), "data": {}}),
            )
            mock.put(
                gazu.client.get_full_url("data/entities/%s" % fakeid("shot-1")),
                text=json.dumps(
                    {"id": fakeid("shot-1"), "data": {"metadata-1": "metadata-1"}}
                ),
            )
            data = {"metadata-1": "metadata-1"}
            shot = gazu.shot.update_shot_data(fakeid("shot-1"), data)
            self.assertEqual(shot["data"]["metadata-1"], "metadata-1")

    def test_update_sequence_data(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/sequences/%s" % fakeid("sequence-1")),
                text=json.dumps({"id": fakeid("sequence-1"), "data": {}}),
            )
            mock.put(
                gazu.client.get_full_url("data/entities/%s" % fakeid("sequence-1")),
                text=json.dumps(
                    {"id": fakeid("sequence-1"), "data": {"metadata-1": "metadata-1"}}
                ),
            )
            data = {"metadata-1": "metadata-1"}
            sequence = gazu.shot.update_sequence_data(fakeid("sequence-1"), data)
            self.assertEqual(sequence["data"]["metadata-1"], "metadata-1")

    def test_update_episode(self):
        with requests_mock.mock() as mock:
            mock.put(
                gazu.client.get_full_url("data/entities/%s" % fakeid("episode-1")),
                text=json.dumps(
                    {"id": fakeid("episode-1"), "project_id": "project-01"}
                ),
            )
            episode = {"id": fakeid("episode-1"), "name": "episode-1"}
            episode = gazu.shot.update_episode(episode)
            self.assertEqual(episode["id"], fakeid("episode-1"))

    def test_update_episode_data(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/sequences/%s" % fakeid("episode-1")),
                text=json.dumps({"id": fakeid("episode-1"), "data": {}}),
            )
            mock.put(
                gazu.client.get_full_url("data/entities/%s" % fakeid("episode-1")),
                text=json.dumps(
                    {"id": fakeid("episode-1"), "data": {"metadata-1": "metadata-1"}}
                ),
            )
            data = {"metadata-1": "metadata-1"}
            episode = gazu.shot.update_episode_data(fakeid("episode-1"), data)
            self.assertEqual(episode["data"]["metadata-1"], "metadata-1")
