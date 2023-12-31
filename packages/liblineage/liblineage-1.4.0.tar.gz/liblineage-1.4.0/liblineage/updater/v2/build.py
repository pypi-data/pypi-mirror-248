#
# Copyright (C) 2023 The LineageOS Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from datetime import datetime
from typing import Any, Dict, List

from liblineage.updater.v2.build_file import BuildFile

class Build:
	"""LineageOS device build informations.

	Attributes:
	- date (str): The date of the build, in ISO 8601 format
	- datetime (datetime): The date of the build, as a date object
	- files (list[BuildFile]): List of files belonging to this build, first one being the OTA zip
	"""
	def __init__(
		self,
		date: str,
		datetime: datetime,
		files: List[BuildFile],
	) -> None:
		self.date = date
		self.datetime = datetime
		self.files = files

		self.ota_zip = self.files[0]

	@classmethod
	def from_json(cls, json: Dict[str, Any]):
		"""Create an object from a JSON object."""

		return cls(
			json["date"],
			datetime.fromtimestamp(json["datetime"]),
			[BuildFile.from_json(file) for file in json["files"]],
		)
