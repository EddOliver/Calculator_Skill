#!/usr/bin/env python3
# -*- coding:utf-8 -*-

### **************************************************************************** ###
#
# Project: Snips Screen Project
# Created Date: Monday, February 11th 2019, 2:46:14 pm
# Author: Greg
# -----
# Last Modified: Sun Mar 03 2019
# Modified By: Greg
# -----
# Copyright (c) 2019 Greg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
### **************************************************************************** ###


from enum import Enum


class textAlignment(Enum):
    LEFT = 'text-left'
    CENTER = 'text-center'
    RIGHT = 'text-right'


class cardStackTypes(Enum):
    GROUP = 'group'
    DECK = 'deck'


class bootstrapHeading(Enum):
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"



class ScreenLayoutObjects():
    #    """Snips Screen Application HTML layout items"""

    class Card():

        def __init__(self, cardHeaderText="", cardTitleText="", cardBodyText="", cardFooterText="", textAlign=textAlignment.LEFT, cardClassAdditions="", cardStyle=""):
            self.cardAlignment = textAlign
            self.cardClassAdditions = cardClassAdditions
            self.cardStyle = cardStyle

            self.cardHeaderText = cardHeaderText
            self.cardHeaderClassAdditions = ""
            self.cardHeaderStyle = ""

            self.cardTitleText = cardTitleText
            self.cardTitleClassAdditions = ""
            self.cardTitleStyle = ""

            self.cardBodyClassAdditions = ""
            self.cardBodyStyle = ""

            self.cardBodyText = cardBodyText
            self.cardBodyTextClassAdditions = ""
            self.cardBodyTextStyle = ""

            self.cardFooterText = cardFooterText
            self.cardFooterClassAdditions = ""
            self.cardFooterStyle = ""

        """
        @property
        def cardHeader(self):
            return '<div class="card-header {}" style="{}>{}</div>'.format(self.cardHeaderClassAdditions, self.cardHeaderText, self.cardHeaderStyle)
   
        @cardHeader.setter
        def cardHeader(cardHeaderText, customClassAdditions="", cardHeaderStyle=""):
            self.cardHeaderText = cardHeaderText
            self.cardHeaderClassAdditions = customClassAdditions
            self.cardHeaderStyle = cardHeaderStyle
       
        @property
        def cardTitle(self):
            return '<div class="card-header {}" style="{}>{}</div>'.format(self.cardTitleClassAdditions, self.cardTitleText, self.cardTitleStyle)
        
        @cardTitle.setter
        def cardTitle(cardTitleText, cardTitleClassAdditions="", cardTitleStyle=""):
            self.cardTitleText = cardTitleText
            self.cardTitleClassAdditions = cardTitleClassAdditions
            self.cardTitleStyle = cardTitleStyle
        
        @property
        def cardText(self):
            return '<div class="card-header {}" style="{}>{}</div>'.format(self.cardBodyTextClassAdditions, self.cardBodyText, self.cardBodyTextStyle)
  
        @cardText.setter
        def cardText(cardFooterText, cardFooterClassAdditions="", cardFooterStyle=""):
            self.cardBodyText = cardBodyText
            self.cardBodyTextClassAdditions = cardBodyTextClassAdditions
            self.cardBodyTextStyle = cardBodyTextStyle        

        @property
        def cardFooter(self):
            return '<div class="card-header {}" style="{}>{}</div>'.format(self.cardFooterClassAdditions, self.cardFooterText, self.cardFooterStyle)
        
        @cardFooter.setter
        def cardFooter(cardFooterText, cardFooterClassAdditions="", cardFooterStyle=""):
            self.cardFooterText = cardFooterText
            self.cardFooterClassAdditions = cardFooterClassAdditions
            self.cardFooterStyle = cardFooterStyle
        """

        def generateCard(self):
            html = '<div class="card {} {}" style="{}">'.format(
                self.cardAlignment.value, self.cardClassAdditions, self.cardStyle)
            if not self.cardHeaderText == "":
                html += '<div class="card-header {}" style="{}">{}</div>'.format(
                    self.cardHeaderClassAdditions, self.cardHeaderStyle, self.cardHeaderText)

            html += '<div class="card-body {}" style="{}">'.format(
                self.cardBodyClassAdditions, self.cardBodyStyle)
            if not self.cardTitleText == "":
                html += '<div class="card-title {}" style="{}">{}</div>'.format(
                    self.cardTitleClassAdditions, self.cardTitleStyle, self.cardTitleText)
            html += '<div class="card-text {}" style="{}">{}</div>'.format(
                self.cardBodyTextClassAdditions, self.cardBodyTextStyle, self.cardBodyText)
            html += '</div>'  # end card-body

            if not self.cardFooterText == "":
                html += '<div class="card-footer {}" style="{}">'.format(
                    'text-muted' if self.cardFooterClassAdditions == "" else self.cardFooterClassAdditions, self.cardFooterStyle)
                html += '{}'.format(self.cardFooterText)
                html += '</div>'

            html += '</div>'  # end card

            return html

    class Table():

        def __init__(self, tableClassAdditions="", tableStyle=""):
            self.tableClassAdditions = tableClassAdditions
            self.tableStyle = tableStyle
            self.tableHeader = ""
            self.tableRows = ""

        def tableColumHeaderBuilder(self, columnTitles=[], colCustomClassAdditions="", colStyle=""):
            header = "<thead><tr>"
            for col in range(0, len(columnTitles)):
                header += '<th scope="col {}" style="{}">{}</th>'.format(
                    colCustomClassAdditions, colStyle, col)
            header += "</tr></thead>"
            self.tableHeader = header

        def tableRowBuilder(self, rowItems=[], rowCustomClassAdditions="", rowStyle=""):
            rowHTML = "<tr>"
            for row in range(0, len(rowItems)):
                rowHTML += '<td class="{}" style="{}">{}</td>'.format(
                    rowCustomClassAdditions, rowStyle, row)
            rowHTML += "</tr>"
            self.tableRows += rowHTML  # can build single rows at a time ti use the Class

        def generateTable(self):
            html = '<table class="table {}" style="{}">'.format(
                self.tableClassAdditions, self.tableStyle)
            if not self.tableHeader == "":
                html += self.tableHeader
            html += '<tbody>'
            html += self.tableRows
            html += '</tbody></table>'

            return html


class ScreenLayoutBuilder():
    """ Create the HTML page to display on the Snips Screen App Device """

    def __init__(self, pageHeaderTitle=None, pageHeaderTextAlign=textAlignment.CENTER,
                 pageFooterText=None, pageFooterTextAlign=textAlignment.RIGHT, cssStyle="",
                 pageTimeout=5):
        """Init the builder

        Keyword Arguments:
            pageHeaderTitle {str} -- Title string to display at the top of the page (default: {None})
            pageHeaderTextAlign {textAlignment} -- Position of title, left,center,right (default: {textAlignment.CENTER})
            pageFooterText {str} -- Page footer text (default: {None})
            pageFooterTextAlign {textAlignement} -- Position of text, left,center,right (default: {textAlignment.RIGHT})
            pageTimeout {int} -- Seconds before the page goes blank (default: {5})
        """
        self.cssStyle = "<style>{}</style>".format(cssStyle)
        self.headerHTML = self.buildHeaderTextHTML(
            pageHeaderTitle, pageHeaderTextAlign) if not pageHeaderTitle is None else None
        self.pageContent = "<div></div>"
        self.footerHTML = self.buildFooterTextHTML(
            pageFooterText, pageFooterTextAlign) if not pageFooterText is None else None
        self.pageTimeout = pageTimeout * 1000 if pageTimeout < 100 else pageTimeout

    @staticmethod
    def buildHeaderTextHTML(title, textAlign=textAlignment.CENTER, customClassAdditions=""):
        """HTML Header builder with title

        Arguments:
            title {str} -- title text for page

        Returns:
            str -- HTML Code for Header
        """
        return "<div class='header' style=''><h1 class='ml-2 mr-2 mt-2 mb-2 {} {}'>{}</h1></div>".format(textAlign.value, customClassAdditions, title)

    @staticmethod
    def buildFooterTextHTML(text, textAlign=textAlignment.RIGHT, customClassAdditions=""):
        """HTML Footer builder with text

        Arguments:
            text {str} -- text to display in the footer

        Returns:
            str -- HTML Code for Footer
        """
        return "<div class='footer'><footer class='blockquote-footer mb-1 {} {}'>{}</footer></div>".format(textAlign.value, customClassAdditions, text)

    def generateScreenHTML(self):
        container = self.cssStyle if self.cssStyle.startswith(
            "<style>") else "<style>{}</style>".format(self.cssStyle)

        container += '<div class="grid-container">'
        container += '<div class="header"></div>' if self.headerHTML is None else self.headerHTML
        container += '<div class="main">'
        container += self.pageContent
        container += '</div>'
        container += '<div class="footer"></div>' if self.footerHTML is None else self.footerHTML
        container += '</div>'

        # print(container)
        return container

    def generateGridHTML(self, items=[], numOfGridColumns=1, customClassAdditions="", style="",
                         rowCustomClassAdditions="", rowStyle="",
                         colCustomClassAdditions="", colStyle=""):
        """build the HTML page for the Snips Screen to display to the user

        Keyword Arguments:
            items {list} -- List of ScreenLayoutObjects code to put in the middle  (default: {[]})
            numOfGridColumns {int} -- number of columns in the grid of items to display (default: {1})

         Returns:
            str -- HTML page code to MQTT Publish for the display to show
        """

        # https://getbootstrap.com/docs/4.0/layout/grid/#vertical-alignment
        numOfGridRows = len(items)/numOfGridColumns if len(
            items) % numOfGridColumns == 0 else len(items)/numOfGridColumns + 1
        gridItemsAlign = "align-items-start"
        if numOfGridRows == 1:
            gridItemsAlign = "align-items-center"

        container = "<div class='grid-holder {}' style='{}'>".format(
            customClassAdditions, style)
        for row in range(0, numOfGridRows):
            container += "<div class='row {} {}' style='{}'>".format(
                gridItemsAlign, rowCustomClassAdditions, rowStyle)
            for col in range(0, numOfGridColumns):
                container += "<div class='col {} {}' style='{}'>".format(
                    gridItemsAlign, colCustomClassAdditions, colStyle)
                container += items[0] if len(items) > 0 else "<div></div>"
                if len(items) > 0:
                    items.pop(0)
                container += "</div>"

            container += "</div>"
        container += "</div>"

        self.pageContent = container

        return container

    def generateCardStacksHTML(self, cardItems=[], cardStackType=cardStackTypes.GROUP, customClassAdditions="", style=""):

        container = "<div class='card-{} flex-row {}' style'{}'>".format(
            cardStackType.value, customClassAdditions, style)
        for card in cardItems:
            container += card
        container += "</div>"

        self.pageContent = container

        return container
