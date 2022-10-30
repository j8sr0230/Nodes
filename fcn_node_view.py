# -*- coding: utf-8 -*-
###################################################################################
#
#  fcn_node_view.py
#
#  MIT License
#
#  Copyright (c) 2019, Pavel Křupala
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
#
###################################################################################
"""
A module containing the view class (visual representation) of a node in the node editor application.
"""
from typing import Optional

from PySide2.QtCore import Qt, QRectF, QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent
from PySide2.QtWidgets import QGraphicsItem, QWidget, QGraphicsTextItem, QGraphicsProxyWidget, QStyleOptionGraphicsItem
from PySide2.QtGui import QFont, QColor, QPen, QBrush, QPainterPath, QPainter


class QGraphicsNode(QGraphicsItem):
    """View class of a node in the node editor application.

    The view class QGraphicsNode is a QGraphicsItem to display nodes in QGraphicsScene instances.

    Attributes:
        node: (nodeeditor.node_node.Node): Model class of a node in the graphics scene

        width (int): Current width of the node.
        height (int): Current height of the node.
        collapsed_height (int): Height of the collapsed node.
        default_height (int): Default (uncollapsed) height of the node.
        edge_roundness (int): Roundness of the node corners.
        edge_padding (int): Padding between node and node content.
        title_horizontal_padding (int): Horizontal padding between node and node title.
        title_vertical_padding (int): Vertical padding between node and node title.

        _title (str): Title of the node
        _title_color (QColor): Title color
        _title_font (QFont): Title font
        _color (QColor): Node color
        _color_selected (QColor): Node color for selected nodes
        _color_hovered (QColor): Node color for nodes in hover state
        _pen_default (QPen): Node pen
        _pen_selected (QPen): Node pen for selected nodes
        _pen_hovered (QPen): Node pen for nodes in hover state
        _brush_title (QBrush): Title brush
        _brush_background (QBrush): Background brush

        title_item (QGraphicsTextItem): QWidget to display the node title
        grContent (QGraphicsProxyWidget): QWidget to display the node content
        status_icons (QImage): Icons for the node state (valid, invalid, dirty)
        main_icon (QImage): Main icons of the node

        hovered (bool): Indicates weather a node is in the hover state
        _was_moved (bool): Indicates weather a node was moved
        _last_selected_state (bool): Indicates weather a node was selected
    """

    node: nodeeditor.node_node.Node

    width: int
    height: int
    collapsed_height: int
    default_height: int
    edge_roundness: int
    edge_padding: int
    title_height: int
    title_horizontal_padding: int
    title_vertical_padding: int

    _title: str
    _title_color: QColor
    _title_font: QFont
    _color: QColor
    _color_selected: QColor
    _color_hovered: QColor
    _pen_default: QPen
    _pen_selected: QPen
    _pen_hovered: QPen
    _brush_title: QBrush
    _brush_background: QBrush

    title_item: QGraphicsTextItem
    grContent: QGraphicsProxyWidget
    status_icons: QImage
    main_icon: QImage

    hovered: bool
    _was_moved: bool
    _last_selected_state: bool

    def __init__(self, node: nodeeditor.node_node.Node, parent: QWidget = None):
        """QGraphicsNode constructor

        :param node: Reference to QGraphicsNode model class
        :type node: nodeeditor.node_node.Node
        :param parent: Parent widget
        :type parent: QWidget
        """

        super().__init__(parent)

        self.node: nodeeditor.node_node.Node = node

        self.hovered: bool = False
        self._was_moved: bool = False
        self._last_selected_state: bool = False

        self.init_sizes()
        self.init_assets()
        self.init_ui()

    @property
    def content(self) -> Optional[QWidget]:
        """Reference to the node content"""
        return self.node.content if self.node else None

    @property
    def title(self) -> str:
        """Returns the node title

        :return: Title of the node
        :rtype: str
        """

        return self._title

    @title.setter
    def title(self, title: str) -> None:
        """Sets the node title and updates the title widget

        :param title: The new node title
        :type title: str
        """

        self._title: str = title
        self.title_item.setPlainText(self._title)

    def init_ui(self) -> None:
        """Sets up QGraphicsNode user interface"""

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        self.init_title()
        self.title = self.node.title

        self.init_content()

    def init_sizes(self) -> None:
        """Sets up QGraphicsNode dimensions"""
        self.width: int = 180
        self.height: int = 240
        self.default_height: int = self.height
        self.collapsed_height: int = 50
        self.edge_roundness: int = 10
        self.edge_padding: int = 10
        self.title_height: int = 24
        self.title_horizontal_padding: int = 4
        self.title_vertical_padding: int = 4

    def init_assets(self) -> None:
        """Initialize all necessary QGraphicsNode assets (colors, pens, brushes and icons)"""

        self._title_color: QColor = Qt.white
        self._title_font: QFont = QFont("Ubuntu", 10)

        self._color: QColor = QColor("#7F000000")
        self._color_selected: QColor = QColor("#FFFFA637")
        self._color_hovered: QColor = QColor("#FF37A6FF")

        self._pen_default: QPen = QPen(self._color)
        self._pen_default.setWidthF(2.0)
        self._pen_selected: QPen = QPen(self._color_selected)
        self._pen_selected.setWidthF(2.0)
        self._pen_hovered: QPen = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(3.0)

        self._brush_title: QBrush = QBrush(QColor("#FF313131"))
        self._brush_background: QBrush = QBrush(QColor("#E3212121"))

        path: str = locator.icon("fcn_status_icon.png")
        self.status_icons: QImage = QImage(path)
        self.main_icon: QImage = QImage(self.node.icon)

    def on_selected(self) -> None:
        """Event handling when the node was selected"""

        self.node.scene.grScene.itemSelected.emit()

    def do_select(self, new_state: bool = True) -> None:
        """Safe version of selecting the QGraphicsNode

        This method takes care about the selection state flag used internally.

        :param new_state: True to select, False to deselect
        :type new_state: bool
        """

        self.setSelected(new_state)
        self._last_selected_state: bool = new_state
        if new_state:
            self.on_selected()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """Event to detect that the node was moved

        :param event: Mouse event
        :type event: QGraphicsSceneMouseEvent
        """

        super().mouseMoveEvent(event)

        # Needs improvement: Just update the selected nodes
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()
        self._was_moved: bool = True

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """Event to handle when the node was moved, selected or deselected

        :param event: Mouse event
        :type event: QGraphicsSceneMouseEvent
        """

        super().mouseReleaseEvent(event)

        # When moved
        if self._was_moved:
            self._was_moved: bool = False
            self.node.scene.history.storeHistory("Node moved", setModified=True)

            self.node.scene.resetLastSelectedStates()
            self.do_select()  # Also trigger itemSelected when node was moved

            # Store the last selected state, because moving does also select the nodes
            self.node.scene._last_selected_items = self.node.scene.getSelectedItems()

            # Now we want to skip storing selection
            return

        # When clicked
        if self._last_selected_state != self.isSelected() or \
                self.node.scene._last_selected_items != self.node.scene.getSelectedItems():
            self.node.scene.resetLastSelectedStates()
            self._last_selected_state: bool = self.isSelected()
            self.on_selected()

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """Handles doubleclick event

        :param event: Mouse event
        :type event: QGraphicsSceneMouseEvent
        """

        # Resends event to the model class
        self.node.onDoubleClicked(event)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Handles hover enter event

        :param event: Mouse event
        :type event: QGraphicsSceneMouseEvent
        """

        self.hovered: bool = True
        self.update()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Handles hover leave event

        :param event: Mouse event
        :type event: QGraphicsSceneMouseEvent
        """

        self.hovered: bool = False
        self.update()

    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""

        return QRectF(0, 0, self.width, self.height).normalized()

    def init_title(self) -> None:
        """Set up the title graphics representation"""

        self.title_item: QGraphicsTextItem = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self.title_horizontal_padding, 0)
        self.title_item.setTextWidth(self.width - 2 * self.title_horizontal_padding)

    def init_content(self) -> None:
        """Sets up a container for the node content as QGraphicsProxyWidget"""

        if self.content is not None:
            self.content.setGeometry(self.edge_padding, self.title_height + self.edge_padding,
                                     self.width - 2 * self.edge_padding,
                                     self.height - 2 * self.edge_padding - self.title_height)

        # Get the QGraphicsProxyWidget when inserted into the grScene
        self.grContent: QGraphicsProxyWidget = self.node.scene.grScene.addWidget(self.content)
        self.grContent.node = self.node
        self.grContent.setParentItem(self)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None, **kwargs) -> None:
        """Paints the rounded rectangular node in local coordinates

        :param painter: Painter instance that is performing the drawing
        :type painter: QPainter
        :param option: Style options for the drawing
        :type option: QStyleOptionGraphicsItem
        :param widget: The widget that is being painted on
        :type widget: QWidget
        """

        # Title
        path_title: QPainterPath = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_roundness, self.edge_roundness)
        path_title.addRect(0, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        path_title.addRect(self.width - self.edge_roundness, self.title_height - self.edge_roundness,
                           self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # Content
        path_content: QPainterPath = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height,
                                    self.edge_roundness, self.edge_roundness)
        path_content.addRect(0, self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(self.width - self.edge_roundness, self.title_height,
                             self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # Outline
        path_outline: QPainterPath = QPainterPath()
        path_outline.addRoundedRect(-1, -1, self.width+2, self.height+2, self.edge_roundness, self.edge_roundness)
        painter.setBrush(Qt.NoBrush)

        if self.hovered:
            painter.setPen(self._pen_hovered)
            painter.drawPath(path_outline.simplified())
            painter.setPen(self._pen_default)
            painter.drawPath(path_outline.simplified())
        else:
            painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
            painter.drawPath(path_outline.simplified())

        # Status and main icon
        painter.drawImage(QRectF(-12, -12, 24, 24), self.main_icon, QRectF(self.main_icon.rect()))
        status_icon_placement: QRectF = QRectF(self.width - 12, -12, 24.0, 24.0)
        if self.node.isDirty():
            painter.drawImage(status_icon_placement, self.status_icons, QRectF(0, 0, 24, 24))
        if self.node.isInvalid():
            painter.drawImage(status_icon_placement, self.status_icons, QRectF(48, 0, 24, 24))
