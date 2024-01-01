from pyqliksense.utils.functions import get_random_string


def kpi_definition(measure = None) -> dict:
    return {
            "qInfo": {"qId": get_random_string(5), "qType": "kpi"},
            "qExtendsId": "",
            "qMetaDef": {},
            "qStateName": "",
            "qHyperCubeDef": {
                "qStateName": "",
                "qDimensions": [],
                "qMeasures": [
                    {
                        "qLibraryId": "",
                        "qDef": {
                            "qLabel": "",
                            "qDescription": "",
                            "qTags": [],
                            "qGrouping": "N",
                            "qDef": measure or "",
                            "qNumFormat": {"qType": "U", "qnDec": 10, "qUseThou": 0, "qFmt": "", "qDec": "", "qThou": ""},
                            "qRelative": False,
                            "qBrutalSum": False,
                            "qAggrFunc": "",
                            "qAccumulate": 0,
                            "qReverseSort": False,
                            "qActiveExpression": 0,
                            "qExpressions": [],
                            "qLabelExpression": "",
                            "autoSort": True,
                            "cId": "tjLW",
                            "numFormatFromTemplate": True,
                            "measureAxis": { "min": 0, "max": 100 },
                            "conditionalColoring": {
                                "useConditionalColoring": False,
                                "singleColor": 3,
                                "paletteSingleColor": {
                                    "index": 6
                                },
                                "segments": {
                                    "limits": [],
                                    "paletteColors": [
                                        {
                                            "index": 6
                                        }
                                    ]
                                }
                            }
                        },
                        "qSortBy": {
                            "qSortByState": 0,
                            "qSortByFrequency": 0,
                            "qSortByNumeric": -1,
                            "qSortByAscii": 0,
                            "qSortByLoadOrder": 1,
                            "qSortByExpression": 0,
                            "qExpression": {"qv": ""},
                            "qSortByGreyness": 0
                        },
                        "qAttributeExpressions": [],
                        "qAttributeDimensions": [],
                        "qCalcCond": { "qv": ""},
                        "qCalcCondition": {"qCond": {"qv": ""},"qMsg": {"qv": ""}},
                        "qTrendLines": [],
                        "qMiniChartDef": {
                            "qDef": "",
                            "qLibraryId": "",
                            "qSortBy": {
                                "qSortByState": 0,
                                "qSortByFrequency": 0,
                                "qSortByNumeric": 0,
                                "qSortByAscii": 0,
                                "qSortByLoadOrder": 0,
                                "qSortByExpression": 0,
                                "qExpression": {"qv": ""},
                                "qSortByGreyness": 0
                            },
                            "qOtherTotalSpec": {
                                "qOtherMode": "OTHER_OFF",
                                "qOtherCounted": {"qv": ""},
                                "qOtherLimit": {"qv": ""},
                                "qOtherLimitMode": "OTHER_GT_LIMIT",
                                "qSuppressOther": False,
                                "qForceBadValueKeeping": True,
                                "qApplyEvenWhenPossiblyWrongResult": True,
                                "qGlobalOtherGrouping": False,
                                "qOtherCollapseInnerDimensions": False,
                                "qOtherSortMode": "OTHER_SORT_DESCENDING",
                                "qTotalMode": "TOTAL_OFF",
                                "qReferencedExpression": {"qv": ""}
                            },
                            "qMaxNumberPoints": -1,
                            "qAttributeExpressions": [],
                            "qNullSuppression": False
                        }
                    }
                ],
                "qInterColumnSortOrder": [0],
                "qSuppressZero": False,
                "qSuppressMissing": True,
                "qInitialDataFetch": [{"qLeft": 0, "qTop": 0, "qWidth": 1, "qHeight": 1}],
                "qReductionMode": "N",
                "qMode": "S",
                "qPseudoDimPos": -1,
                "qNoOfLeftDims": -1,
                "qAlwaysFullyExpanded": False,
                "qMaxStackedCells": 5000,
                "qPopulateMissing": False,
                "qShowTotalsAbove": False,
                "qIndentMode": False,
                "qCalcCond": {"qv": ""},
                "qSortbyYValue": 0,
                "qTitle": {"qv": ""},
                "qCalcCondition": {
                    "qCond": {
                        "qv": ""
                    },
                    "qMsg": {
                        "qv": ""
                    }
                },
                "qColumnOrder": [],
                "qExpansionState": [],
                "qDynamicScript": [],
                "qContextSetExpression": "",
                "qSuppressMeasureTotals": False,
                "qLayoutExclude": {
                    "qHyperCubeDef": {
                        "qDimensions": [],
                        "qMeasures": [],
                        "qStateName": "",
                        "qInterColumnSortOrder": [],
                        "qSuppressZero": False,
                        "qSuppressMissing": False,
                        "qInitialDataFetch": [],
                        "qReductionMode": "N",
                        "qMode": "S",
                        "qPseudoDimPos": -1,
                        "qNoOfLeftDims": -1,
                        "qAlwaysFullyExpanded": False,
                        "qMaxStackedCells": 5000,
                        "qPopulateMissing": False,
                        "qShowTotalsAbove": False,
                        "qIndentMode": False,
                        "qCalcCond": {
                            "qv": ""
                        },
                        "qSortbyYValue": 0,
                        "qTitle": {
                            "qv": ""
                        },
                        "qCalcCondition": {
                            "qCond": {
                                "qv": ""
                            },
                            "qMsg": {
                                "qv": ""
                            }
                        },
                        "qColumnOrder": [],
                        "qExpansionState": [],
                        "qDynamicScript": [],
                        "qContextSetExpression": "",
                        "qSuppressMeasureTotals": False
                    }
                }
            },
            "script": "",
            "showTitles": False,
            "title": "",
            "subtitle": "",
            "footnote": "",
            "disableNavMenu": True,
            "showDetails": True,
            "showDetailsExpression": False,
            "useLink": False,
            "sheetLink": "",
            "openUrlInNewTab": True,
            "tooltip": {
                "hideBasic": False,
                "chart": {"style": {"size": "medium"}}
            },
            "visualization": "kpi",
            "version": "0.13.4",
            "showMeasureTitle": True,
            "showSecondMeasureTitle": True,
            "textAlign": "center",
            "layoutBehavior": "relative",
            "fontSize": "M",
            "components": []
        }