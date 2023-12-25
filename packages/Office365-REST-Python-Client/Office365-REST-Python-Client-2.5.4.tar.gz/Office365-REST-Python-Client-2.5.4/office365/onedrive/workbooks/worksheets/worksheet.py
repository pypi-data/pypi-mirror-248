from typing import Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.workbooks.charts.chart import WorkbookChart
from office365.onedrive.workbooks.names.named_item import WorkbookNamedItem
from office365.onedrive.workbooks.tables.collection import WorkbookTableCollection
from office365.onedrive.workbooks.tables.pivot_table import WorkbookPivotTable
from office365.onedrive.workbooks.worksheets.protection import (
    WorkbookWorksheetProtection,
)
from office365.runtime.paths.resource_path import ResourcePath


class WorkbookWorksheet(Entity):
    """
    An Excel worksheet is a grid of cells. It can contain data, tables, charts, etc
    """

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def charts(self):
        # type: () -> EntityCollection[WorkbookChart]
        """Returns collection of charts that are part of the worksheet"""
        return self.properties.get(
            "charts",
            EntityCollection(
                self.context, WorkbookChart, ResourcePath("charts", self.resource_path)
            ),
        )

    @property
    def name(self):
        # type: () -> Optional[str]
        """The display name of the worksheet."""
        return self.properties.get("name", None)

    @property
    def names(self):
        # type: () -> EntityCollection[WorkbookNamedItem]
        """Returns collection of names that are associated with the worksheet"""
        return self.properties.get(
            "names",
            EntityCollection(
                self.context,
                WorkbookNamedItem,
                ResourcePath("names", self.resource_path),
            ),
        )

    @property
    def tables(self):
        # type: () -> WorkbookTableCollection
        """Collection of tables that are part of the worksheet."""
        return self.properties.get(
            "tables",
            WorkbookTableCollection(
                self.context, ResourcePath("tables", self.resource_path)
            ),
        )

    @property
    def pivot_tables(self):
        # type: () -> EntityCollection[WorkbookPivotTable]
        """Collection of PivotTables that are part of the worksheet."""
        return self.properties.get(
            "pivotTables",
            EntityCollection(
                self.context,
                WorkbookPivotTable,
                ResourcePath("pivotTables", self.resource_path),
            ),
        )

    @property
    def protection(self):
        # type: () -> WorkbookWorksheetProtection
        """Returns sheet protection object for a worksheet."""
        return self.properties.get(
            "protection",
            WorkbookWorksheetProtection(
                self.context, ResourcePath("protection", self.resource_path)
            ),
        )

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "pivotTables": self.pivot_tables,
            }
            default_value = property_mapping.get(name, None)
        return super(WorkbookWorksheet, self).get_property(name, default_value)
