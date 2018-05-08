import BruteJusticeGrid as grid
import BruteJusticeSpreadsheets
gridSheetID = '1-DjsyCbph0tw4Esg87pEApyp-NZn3B6yx5A6nk3uYUs'
icons = grid.icons



gridImage = grid.LabelGrid(grid.GridFromArray(BruteJusticeSpreadsheets.ReadSpreadsheet('Sheet1', gridSheetID), grid.HexagonImage()))
gridImage.show()