#!/usr/bin/env python3

from lxml import etree as et  # for reading TEI XML inputs

from .common import xml_ns, tei_ns
from .reading import Reading


class VariationUnit:
    """Base class for storing TEI XML variation unit data internally.

    This corresponds to an app element in the collation.

    Attributes:
        id: The ID string of this variation unit, which should be unique.
        readings: A list of Readings contained in this VariationUnit.
        intrinsic_relations: A dictionary mapping pairs of IDs of Readings in this VariationUnit to the intrinsic odds category
        describing the two readings' relative probability of being authorial.
        transcriptional_relations: A dictionary mapping pairs of IDs of Readings in this VariationUnit to a set of transcriptional change categories
        that could explain the rise of the second reading from the first.
    """

    def __init__(self, xml: et.Element, verbose: bool = False):
        """Constructs a new VariationUnit instance from the TEI XML input.

        Args:
            xml: An lxml.etree.Element representing an app element.
            verbose: An optional boolean flag indicating whether or not to print status updates.
        """
        # Use its xml:id if it has one; otherwise, use its n attribute if it has one:
        self.id = ""
        if xml.get("{%s}id" % xml_ns) is not None:
            self.id = xml.get("{%s}id" % xml_ns)
        elif xml.get("n") is not None:
            self.id = xml.get("n")
        # Initialize its list of readings:
        self.readings = []
        # Initialize its dictionaries of intrinsic and transcriptional relations:
        self.intrinsic_relations = {}
        self.transcriptional_relations = {}
        # Now parse the app element to populate these data structures:
        self.parse(xml, verbose)
        if verbose:
            print("New VariationUnit %s with %d readings" % (self.id, len(self.readings)))

    def __str__(self):
        return self.id

    def __repr__(self):
        return str(self)

    def parse(self, xml: et.Element, verbose: bool = False):
        """Given an XML element, recursively parses its subelements for readings, reading groups, and witness details.

        Other children of app elements, such as note, noteGrp, and wit elements, are ignored.

        Args:
            xml: An lxml.etree.Element representing an app element.
            verbose: An optional boolean flag indicating whether or not to print status updates.
        """
        # Determine what this element is:
        raw_tag = xml.tag.replace("{%s}" % tei_ns, "")
        # If it is an apparatus, then initialize the readings list and process the child elements of the apparatus recursively:
        if raw_tag == "app":
            self.readings = []
            for child in xml:
                self.parse(child, verbose)
            return
        # If it is a reading group, then flatten it by processing its children recursively, applying the reading group's type to the readings contained in it:
        if raw_tag == "rdgGrp":
            # Get the type of this reading group:
            reading_group_type = xml.get("type") if xml.get("type") is not None else None
            for child in xml:
                child_raw_tag = child.tag.replace("{%s}" % tei_ns, "")
                if child_raw_tag in [
                    "lem",
                    "rdg",
                ]:  # any <lem> element in a <rdgGrp> can be assumed not to be a duplicate of a <rdg> element, as there should be only one <lem> at all levels under an <app> element
                    rdg = Reading(child, verbose)
                    if rdg.type is not None:
                        rdg.type = reading_group_type
                    self.readings.append(rdg)
                else:
                    self.parse(child, verbose)
            return
        # If it is a lemma, then add it as a reading if has its own witness list (even if that list is empty, which may occur for a conjecture);
        # otherwise, assume its reading is duplicated in a <rdg> element and skip it:
        if raw_tag == "lem":
            if xml.get("wit") is not None:
                lem = Reading(xml, verbose)
                self.readings.append(lem)
            return
        # If it is a reading, then add it as a reading:
        elif raw_tag == "rdg":
            rdg = Reading(xml, verbose)
            self.readings.append(rdg)
            return
        # If it is a witness detail, then add it as a reading, and if it does not have any targeted readings, then add a target for the previous rdg element (per the TEI Guidelines §12.1.4.1):
        elif raw_tag == "witDetail":
            witDetail = Reading(xml, verbose)
            if len(witDetail.targets) == 0 and len(self.readings) > 0:
                previous_rdg_ind = -1
                previous_rdg = self.readings[previous_rdg_ind]
                while len(previous_rdg.targets) > 0:
                    previous_rdg_ind -= 1
                    previous_rdg = self.readings[previous_rdg_ind]
                witDetail.targets.append(previous_rdg.id)
                witDetail.certainties[previous_rdg.id] = 1
            self.readings.append(witDetail)
            return
        # If it is a note, then process the child elements of the note recursively:
        elif raw_tag == "note":
            for child in xml:
                self.parse(child, verbose)
            return
        # If it is a list of relations, then populate the corresponding dictionary:
        elif raw_tag == "listRelation":
            if xml.get("type") is not None and xml.get("type") == "intrinsic":
                self.intrinsic_relations = {}
                for child in xml:
                    if child.get("active") is None or child.get("passive") is None or child.get("ana") is None:
                        continue
                    from_readings = child.get("active").replace("#", "").split()
                    to_readings = child.get("passive").replace("#", "").split()
                    intrinsic_category = (
                        child.get("ana").replace("#", "").split()[0]
                    )  # there shouldn't be more than one of these
                    # For each pair of readings, assign them the specified category
                    for from_reading in from_readings:
                        for to_reading in to_readings:
                            pair = (from_reading, to_reading)
                            self.intrinsic_relations[pair] = intrinsic_category
                return
            if xml.get("type") is not None and xml.get("type") == "transcriptional":
                self.transcriptional_relations = {}
                for child in xml:
                    if child.get("active") is None or child.get("passive") is None or child.get("ana") is None:
                        continue
                    from_readings = child.get("active").replace("#", "").split()
                    to_readings = child.get("passive").replace("#", "").split()
                    transcriptional_categories = child.get("ana").replace("#", "").split()
                    # For each pair of readings, assign them the specified category
                    for from_reading in from_readings:
                        for to_reading in to_readings:
                            pair = (from_reading, to_reading)
                            if pair not in self.transcriptional_relations:
                                self.transcriptional_relations[
                                    pair
                                ] = set()  # we only need distinct categories for each transition
                            for transcriptional_category in transcriptional_categories:
                                self.transcriptional_relations[pair].add(transcriptional_category)
                return
            return
