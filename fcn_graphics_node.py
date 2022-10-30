# -*- coding: utf-8 -*-
###################################################################################
#
#  fcn_graphics_node.py
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
A module containing the visual representation of a node in the graphics scene.
"""
from PySide2.QtCore import Qt, QRectF
from PySide2.QtWidgets import QGraphicsItem, QWidget, QGraphicsTextItem
from PySide2.QtGui import QFont, QColor, QPen, QBrush, QPainterPath


class QGraphicsNode(QGraphicsItem):
    """Visual representation of a node in the graphics scene.

    The visual node is a QGraphicsItem that is display in a QGraphicsScene instance. In addition, it serves as a
    container for the visual node content (see FCNNodeContentView class).The FCNNodeView class specifies all the
    necessary geometric information needed, to display a node in the scene.

    Attributes:
        width (int): Current width of the node.
        height (int): Current height of the node.
        collapsed_height (int): Height of the collapsed node.
        default_height (int): Default (uncollapsed) height of the node.
        edge_roundness (int): Roundness of the node corners.
        edge_padding (int): Padding between node and node content.
        title_horizontal_padding (int): Horizontal padding between node and node title.
        title_vertical_padding (int): Vertical padding between node and node title.
        icons (QImage): Status icons of the node, that is displayed in the top left corner.
    """

    node: nodeeditor.node_node.Node
    hovered: bool
    _was_moved: bool
    _last_selected_state: bool
    _title: str
    width: int
    height: int
    edge_roundness: int
    edge_padding: int
    title_height: int
    title_horizontal_padding: int
    title_vertical_padding: int
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

    collapsed_height: int
    default_height: int

    icons: QImage
    main_icon: QImage

    def __init__(self, node: nodeeditor.node_node.Node, parent: QWidget = None):
        """QGraphicsNode constructor

        :param node: Reference to QGraphicsNode model class
        :type node: nodeeditor.node_node.Node
        :param parent: Parent widget
        :type parent: QWidget
        """

        super().__init__(parent)

        self.node = node

        # Init node state flags
        self.hovered = False
        self._was_moved = False
        self._last_selected_state = False

        self.init_sizes()
        self.init_assets()
        self.init_ui()

    @property
    def content(self):
        """Reference to `Node Content`"""
        return self.node.content if self.node else None

    @property
    def title(self):
        """title of this `Node`

        :getter: current Graphics Node title
        :setter: stores and make visible the new title
        :type: str
        """
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def init_ui(self):
        """Set up this ``QGraphicsItem``"""
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        # init title
        self.init_title()
        self.title = self.node.title

        self.init_content()

    def init_sizes(self):
        """Set up internal attributes like `width`, `height`, etc."""
        self.width = 180
        self.height = 240
        self.edge_roundness = 10
        self.edge_padding = 10
        self.title_height = 24
        self.title_horizontal_padding = 4
        self.title_vertical_padding = 4

        self.default_height: int = self.height
        self.collapsed_height: int = 50

    def init_assets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)

        self._color = QColor("#7F000000")
        self._color_selected = QColor("#FFFFA637")
        self._color_hovered = QColor("#FF37A6FF")

        self._pen_default = QPen(self._color)
        self._pen_selected: QPen
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(3.0)

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

        path: str = locator.icon("fcn_status_icon.png")
        self.icons: QImage = QImage(path)
        self.main_icon: QImage = QImage(self.node.icon)

    def on_selected(self):
        """Our event handling when the node was selected"""
        self.node.scene.grScene.itemSelected.emit()

    def do_select(self, new_state=True):
        """Safe version of selecting the `Graphics Node`. Takes care about the selection state flag used internally

        :param new_state: ``True`` to select, ``False`` to deselect
        :type new_state: ``bool``
        """
        self.setSelected(new_state)
        self._last_selected_state = new_state
        if new_state:
            self.onSelected()

    def mouseMoveEvent(self, event):
        """Overridden event to detect that we moved with this `Node`"""
        super().mouseMoveEvent(event)

        # optimize me! just update the selected nodes
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()
        self._was_moved = True

    def mouseReleaseEvent(self, event):
        """Overriden event to handle when we moved, selected or deselected this `Node`"""
        super().mouseReleaseEvent(event)

        # handle when grNode moved
        if self._was_moved:
            self._was_moved = False
            self.node.scene.history.storeHistory("Node moved", setModified=True)

            self.node.scene.resetLastSelectedStates()
            self.doSelect()     # also trigger itemSelected when node was moved

            # we need to store the last selected state, because moving does also select the nodes
            self.node.scene._last_selected_items = self.node.scene.getSelectedItems()

            # now we want to skip storing selection
            return

        # handle when grNode was clicked on
        if self._last_selected_state != self.isSelected() or \
                self.node.scene._last_selected_items != self.node.scene.getSelectedItems():
            self.node.scene.resetLastSelectedStates()
            self._last_selected_state = self.isSelected()
            self.onSelected()

    def mouseDoubleClickEvent(self, event):
        """Overriden event for doubleclick. Resend to `Node::onDoubleClicked`"""
        self.node.onDoubleClicked(event)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """Handle hover effect"""
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """Handle hover effect"""
        self.hovered = False
        self.update()

    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return QRectF(0, 0, self.width, self.height).normalized()

    def init_title(self):
        """Set up the title Graphics representation: font, color, position, etc."""
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self.title_horizontal_padding, 0)
        self.title_item.setTextWidth(
            self.width
            - 2 * self.title_horizontal_padding
        )

    def init_content(self):
        """Set up the `grContent` - ``QGraphicsProxyWidget`` to have a container for `Graphics Content`"""
        if self.content is not None:
            self.content.setGeometry(self.edge_padding, self.title_height + self.edge_padding,
                                     self.width - 2 * self.edge_padding, self.height - 2 * self.edge_padding -
                                     self.title_height)

        # get the QGraphicsProxyWidget when inserted into the grScene
        self.grContent = self.node.scene.grScene.addWidget(self.content)
        self.grContent.node = self.node
        self.grContent.setParentItem(self)

    def paint(self, painter, option, widget=None, **kwargs):
        """Painting the rounded rectangular `Node`
        :param widget:
        :type widget:
        :param option:
        :type option:
        :type painter: object:
        """
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_roundness, self.edge_roundness)
        path_title.addRect(0, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        path_title.addRect(self.width - self.edge_roundness, self.title_height - self.edge_roundness,
                           self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height,
                                    self.edge_roundness, self.edge_roundness)
        path_content.addRect(0, self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(self.width - self.edge_roundness, self.title_height, self.edge_roundness,
                             self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
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

        painter.drawImage(QRectF(-12, -12, 24, 24), self.main_icon, QRectF(self.main_icon.rect()))
        status_icon_placement = QRectF(self.width - 12, -12, 24.0, 24.0)
        if self.node.isDirty():
            painter.drawImage(status_icon_placement, self.icons, QRectF(0, 0, 24, 24))
        if self.node.isInvalid():
            painter.drawImage(status_icon_placement, self.icons, QRectF(48, 0, 24, 24))
