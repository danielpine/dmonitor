var chart_store = {}

function render(id, xdata, series, title) {
    option = {
        grid: {
            // top: "0px",
            // bottom: "0px",
            left: "70px",
            right: "60px",
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                snap: true,
                label: {
                    margin: 50,
                }
            },
            formatter: (params) => {
                params.sort(function (a, b) {
                    return b.data[1] - a.data[1]
                })
                var d = []
                d.push(formatdate(params[0].axisValue))
                params.forEach(e => {
                    d.push('<div style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:' + e.color + ';"></div> ' + e.seriesName + ' : ' + e.data[1] + '')
                })
                return d.join('<br>')
            },
            extraCssText: 'box-shadow: 0 0 3px rgba(0, 0, 0, 0.3);',
            position: function (pt) {
                return [pt[0], '10%'];
            }
        },
        title: {
            left: 'center',
            text: title,
        },
        legend: {
            type: 'scroll',
            selectedMode: 'multiple',
            icon: 'path://M19,11H5a1,1,0,0,0,0,2H19a1,1,0,0,0,0-2Z',
            selector: ['all', 'inverse'],
            left: 'left',
            align: 'left',
            bottom: 0,
            orient: 'horizontal'
        },
        toolbox: {
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                restore: {},
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'time',
            boundaryGap: false,
            interval: vm.lastTimeOptions[vm.lastTimeOption] * 12 * 1000,
            data: xdata,
            axisLabel: {
                formatter: function (value, index) {
                    return formatdate(value);
                }
            },
            axisPointer: {
                lineStyle: {
                    color: '#004E52',
                    opacity: 0.5,
                    width: 2
                },
                label: {
                    show: true,
                    formatter: function (params) {
                        return echarts.format.formatTime('yyyy-MM-dd hh:mm:ss', params.value);
                    },
                    backgroundColor: '#004E52'
                }
            },
        },
        yAxis: {
            type: 'value',
            boundaryGap: [0, '100%']
        },
        dataZoom: [{
            type: 'inside',
            throttle: 50
        }],
        series: series
    }
    if (!chart_store[id]) {
        chart_store[id] = echarts.init(document.getElementById(id), null, {
            // renderer: 'svg',
        })
    }
    chart_store[id].setOption(option)
}
var resizeDebounce = null;
window.addEventListener('resize', function () {
    function resizePlot() {
        Object.values(chart_store).forEach(chart => chart.resize())
    }
    if (resizeDebounce) {
        window.clearTimeout(resizeDebounce);
    }
    resizeDebounce = window.setTimeout(resizePlot, 100);
});

function pushData(map, pid, t, val) {
    if (!map[pid]) {
        map[pid] = []
    }
    map[pid].push([t, val])
}

function rgb2hex(item) {
    if (item && item.length == 3) {
        var a = item[0],
            b = item[1],
            c = item[2],
            d = "#",
            cArray = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"];
        d += cArray[Math.floor(a / 16)] + "" + cArray[a % 16] + "";
        d += cArray[Math.floor(b / 16)] + "" + cArray[b % 16] + "";
        d += cArray[Math.floor(c / 16)] + "" + cArray[c % 16] + "";
        return d;
    }
}

function genSeries(data_map) {
    var series = []
    for (pid in data_map) {
        var rgb = colorHash.rgb(pid)
        var color = rgb2hex(rgb)
        series.push({
            name: pid,
            type: 'line',
            smooth: true,
            symbol: 'none',
            showSymbol: false,
            sampling: 'average',
            itemStyle: {
                color: color
            },
            lineStyle: {
                width: 1
            },
            areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(' + rgb[0] + ',' + rgb[1] + ', ' + rgb[2] + ', 0.1)'
                }])
            },
            data: data_map[pid]
        })
    }
    return series
}

