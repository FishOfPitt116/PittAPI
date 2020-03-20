"""
The Pitt API, to access workable data of the University of Pittsburgh
Copyright (C) 2015 Ritwik Gupta
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import unittest

from PittAPI import sports

@unittest.skip
class LibraryTest(unittest.TestCase):
    def test_get_mens_basketball_record(self):
        self.assertIsInstance(sports.get_mens_basketball_record(), str)

    def test_get_next_mens_basketball_game(self):
        self.assertIsInstance(sports.get_next_mens_basketball_game(), dict)

    def test_get_mens_basketball_standings(self):
        self.assertRaises(sports.get_mens_basketball_standings(), str)

    def test_get_football_record(self):
        self.assertIsInstance(sports.get_football_record(), str)

    def test_get_next_football_game(self):
        self.assertIsInstance(sports.get_next_football_game(), dict)

    def test_get_football_standings(self):
        self.assertRaises(sports.get_football_standings(), str)
