#      Openfoot Manager - A free and open source soccer management game
#      Copyright (C) 2020-2022  Pedrenrique G. Guimarães
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os

from dataclasses import dataclass
from ofm.defaults import PROJECT_DIR


@dataclass
class Settings:
    res: str = os.path.join(PROJECT_DIR, "res")
    images: str = os.path.join(PROJECT_DIR, "images")
    db: str = os.path.join(PROJECT_DIR, "db")
    save: str = os.path.join(PROJECT_DIR, "save")


