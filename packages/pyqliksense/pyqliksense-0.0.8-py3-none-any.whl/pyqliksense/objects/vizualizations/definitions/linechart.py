from pyqliksense.utils.functions import get_random_string


def linechart_definition(dimensions: list = None, measures: list = None):
    return {
        "qInfo": {"qId": get_random_string(5), "qType": "linechart"},
        "qExtendsId": "",
        "qMetaDef": {},
        "qStateName": "",
        "qHyperCubeDef": {
            "qStateName": "",
            "qDimensions": [{
                "qLibraryId": "",
                "qDef": {
                    "qGrouping": "N",
                    "qFieldDefs": [d],
                    "qFieldLabels": [""],
                    "qSortCriterias": [
                        {
                            "qSortByState": 0,
                            "qSortByFrequency": 0,
                            "qSortByNumeric": 1,
                            "qSortByAscii": 1,
                            "qSortByLoadOrder": 1,
                            "qSortByExpression": 0,
                            "qExpression": {
                                "qv": ""
                            },
                            "qSortByGreyness": 0
                        }
                    ],
                    "qNumberPresentations": [],
                    "qReverseSort": False,
                    "qActiveField": 0,
                    "qLabelExpression": "",
                    "autoSort": True,
                    "cId": "CsaGKZr",
                    "othersLabel": "Others"
                },
                "qNullSuppression": False,
                "qIncludeElemValue": False,
                "qOtherTotalSpec": {
                    "qOtherMode": "OTHER_OFF",
                    "qOtherCounted": {
                        "qv": "10"
                    },
                    "qOtherLimit": {
                        "qv": "0"
                    },
                    "qOtherLimitMode": "OTHER_GE_LIMIT",
                    "qSuppressOther": False,
                    "qForceBadValueKeeping": True,
                    "qApplyEvenWhenPossiblyWrongResult": True,
                    "qGlobalOtherGrouping": False,
                    "qOtherCollapseInnerDimensions": False,
                    "qOtherSortMode": "OTHER_SORT_DESCENDING",
                    "qTotalMode": "TOTAL_OFF",
                    "qReferencedExpression": {
                        "qv": ""
                    }
                },
                "qShowTotal": False,
                "qShowAll": False,
                "qOtherLabel": {
                    "qv": "Others"
                },
                "qTotalLabel": {
                    "qv": ""
                },
                "qCalcCond": {
                    "qv": ""
                },
                "qAttributeExpressions": [],
                "qAttributeDimensions": [],
                "qCalcCondition": {
                    "qCond": {
                        "qv": ""
                    },
                    "qMsg": {
                        "qv": ""
                    }
                }
            } for d in dimensions or []],
            "qMeasures": [{
                "qLibraryId": "",
                "qDef": {
                    "qLabel": "",
                    "qDescription": "",
                    "qTags": [],
                    "qGrouping": "N",
                    "qDef": m,
                    "qNumFormat": {
                        "qType": "U",
                        "qnDec": 10,
                        "qUseThou": 0,
                        "qFmt": "",
                        "qDec": "",
                        "qThou": ""
                    },
                    "qRelative": False,
                    "qBrutalSum": False,
                    "qAggrFunc": "",
                    "qAccumulate": 0,
                    "qReverseSort": False,
                    "qActiveExpression": 0,
                    "qExpressions": [],
                    "qLabelExpression": "",
                    "autoSort": True,
                    "cId": "jZJzThq",
                    "numFormatFromTemplate": True,
                    "styling": []
                },
                "qSortBy": {
                    "qSortByState": 0,
                    "qSortByFrequency": 0,
                    "qSortByNumeric": -1,
                    "qSortByAscii": 0,
                    "qSortByLoadOrder": 1,
                    "qSortByExpression": 0,
                    "qExpression": {
                        "qv": ""
                    },
                    "qSortByGreyness": 0
                },
                "qAttributeExpressions": [],
                "qAttributeDimensions": [],
                "qCalcCond": {
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
                        "qExpression": {
                            "qv": ""
                        },
                        "qSortByGreyness": 0
                    },
                    "qOtherTotalSpec": {
                        "qOtherMode": "OTHER_OFF",
                        "qOtherCounted": {
                            "qv": ""
                        },
                        "qOtherLimit": {
                            "qv": ""
                        },
                        "qOtherLimitMode": "OTHER_GT_LIMIT",
                        "qSuppressOther": False,
                        "qForceBadValueKeeping": True,
                        "qApplyEvenWhenPossiblyWrongResult": True,
                        "qGlobalOtherGrouping": False,
                        "qOtherCollapseInnerDimensions": False,
                        "qOtherSortMode": "OTHER_SORT_DESCENDING",
                        "qTotalMode": "TOTAL_OFF",
                        "qReferencedExpression": {
                            "qv": ""
                        }
                    },
                    "qMaxNumberPoints": -1,
                    "qAttributeExpressions": [],
                    "qNullSuppression": False
                }
            } for m in measures or []],
            "qInterColumnSortOrder": [i for i in range(len(dimensions))],
            "qSuppressZero": False,
            "qSuppressMissing": True,
            "qInitialDataFetch": [{"qLeft": 0, "qTop": 0, "qWidth": 17, "qHeight": 500}],
            "qReductionMode": "N",
            "qMode": "K",
            "qPseudoDimPos": -1,
            "qNoOfLeftDims": -1,
            "qAlwaysFullyExpanded": True,
            "qMaxStackedCells": 5000,
            "qPopulateMissing": False,
            "qShowTotalsAbove": False,
            "qIndentMode": False,
            "qCalcCond": {"qv": ""},
            "qSortbyYValue": 0,
            "qTitle": {"qv": ""},
            "qCalcCondition": {
                "qCond": {"qv": ""},
                "qMsg": {"qv": ""}
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
        "refLine": {
            "refLines": [],
            "dimRefLines": []
        },
        "showTitles": True,
        "title": "",
        "subtitle": "",
        "footnote": "",
        "disableNavMenu": False,
        "showDetails": True,
        "showDetailsExpression": False,
        "showDisclaimer": True,
        "lineType": "line",
        "stackedArea": False,
        "separateStacking": True,
        "orientation": "horizontal",
        "scrollbar": "miniChart",
        "scrollStartPos": 0,
        "nullMode": "gap",
        "dataPoint": {
            "show": False,
            "showLabels": False
        },
        "maxNumPoints": 2000,
        "maxNumLines": 12,
        "gridLine": {"auto": True, "spacing": 2},
        "color": {
            "auto": True,
            "mode": "primary",
            "formatting": {"numFormatFromTemplate": True},
            "useBaseColors": "off",
            "paletteColor": {"index": 6},
            "useDimColVal": True,
            "useMeasureGradient": True,
            "persistent": True,
            "expressionIsColor": True,
            "expressionLabel": "",
            "measureScheme": "sg",
            "reverseScheme": False,
            "dimensionScheme": "12",
            "autoMinMax": True,
            "measureMin": 0,
            "measureMax": 10
        },
        "legend": {"show": True, "dock": "auto", "showTitle": True},
        "dimensionAxis": {
            "continuousAuto": True,
            "show": "all",
            "label": "auto",
            "dock": "near",
            "axisDisplayMode": "auto",
            "maxVisibleItems": 10
        },
        "preferContinuousAxis": True,
        "measureAxis": {
            "show": "all",
            "dock": "near",
            "spacing": 1,
            "autoMinMax": True,
            "minMax": "min",
            "min": 0,
            "max": 10,
            "logarithmic": False
        },
        "tooltip": {
            "auto": True,
            "hideBasic": False,
            "chart": {"style": {"size": "medium"}},
            "title": "",
            "description": ""
        },
        "visualization": "linechart",
        "version": "1.30.3",
        "components": [],
        "showMiniChartForContinuousAxis": True
    }
