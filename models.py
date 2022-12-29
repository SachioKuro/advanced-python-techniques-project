"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from __future__ import annotations
from datetime import datetime
from re import I

from helpers import cd_to_datetime, datetime_to_str

from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional


@dataclass(frozen=True, eq=True, order=True)
class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    designation: str = field(hash=True, compare=True, default='')
    name: Optional[str] = field(hash=False, compare=False, default=None)
    diameter: float = field(hash=False, compare=False, default=float('nan'))
    hazardous: bool = field(hash=False, compare=False, default=False)

    approaches: list[CloseApproach] = field(default_factory=list, hash=False, compare=False, repr=False)

    def __post_init__(self) -> None:
        """Perform initialization after all instance attributes have been set."""
        # if name is empty string set it to None
        object.__setattr__(self, "name", self.name or None)

    @property
    def fullname(self) -> str:
        """Return a representation of the full name of this NEO."""
        return f"{self.designation} [{self.name}]" if self.name else self.designation

    def to_dict(self) -> dict[str, Any]:
        """Return a dict containing the fields of this NEO."""
        return {
            "designation": self.designation,
            "name": self.name or "",
            "diameter_km": self.diameter,
            "potentially_hazardous": self.hazardous,
        }

    def __str__(self) -> str:
        """Return `str(self)`."""
        return (f"{self.fullname} with a diameter of {self.diameter:.3f} km and "
                f"{'is' if self.hazardous else 'is not'} potentially hazardous")


@dataclass(frozen=True, eq=True, order=True)
class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    _designation: str = field(hash=True, compare=True, default="")
    time: Optional[datetime] = field(hash=True, compare=True, default=None)
    distance: float = field(hash=False, compare=False, default=float("nan"))
    velocity: float = field(hash=False, compare=False, default=float("nan"))

    neo: Optional[NearEarthObject] = None

    def __post_init__(self) -> None:
        """Perform initialization after all instance attributes have been set."""
        object.__setattr__(self, "time", cd_to_datetime(self.time))

    @property
    def time_str(self) -> str:
        """Return a formatted representation of this `CloseApproach`'s approach time."""
        return datetime_to_str(self.time)

    def update_neo(self, value: NearEarthObject) -> None:
        """
            Set the value of `self.neo`.
            Use this method to update the NEO reference of the frozen `CloseApproach` object.
        """
        object.__setattr__(self, "neo", value)

    def serialize(self) -> dict[str, str]:
        """Return a dict containing the data in this object."""
        if self.neo is None:
            raise ValueError("Cannot serialize a CloseApproach object with no NEO reference")
        return {
            "datetime_utc": self.time_str,
            "distance_au": str(self.distance),
            "velocity_km_s": str(self.velocity),
            "designation": self.neo.designation,
            "name": self.neo.name or "",
            "diameter_km": str(self.neo.diameter),
            "potentially_hazardous": str(self.neo.hazardous),
        }

    def to_dict(self) -> dict[str, Any]:
        """Return a dict containing the fields of this `CloseApproach`."""
        return {
            "datetime_utc": self.time_str,
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
            "neo": self.neo.to_dict(),
        }

    def __str__(self):
        """Return `str(self)`."""
        if self.neo:
            return (f"At {self.time_str}, '{self.neo.fullname if self.neo else self._designation}'"
                    f" approaches Earth at a distance of {self.distance:.2f} au and "
                    f"a velocity of {self.velocity:.2f} km/s")

