function render(id, xdata, series, title) {
    option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                snap: true,
                label: {
                    margin: 20,
                }
            },
            formatter: (params) => {
                params.sort(function (a, b) {
                    return b.data[1] - a.data[1]
                })
                var d = []
                d.push(formatdate(params[0].axisValue) + '<br>')
                params.forEach(e => {
                    d.push('<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:' + e.color + ';"></span> ' + e.seriesName + ' : ' + e.data[1])
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
    var chart = echarts.init(document.getElementById(id))
    chart.setOption(option, true)
}

function pushData(map, pid, t, val) {
    if (!map[pid]) {
        map[pid] = []
    }
    map[pid].push([t, val])
}

function genSeries(data_map) {
    var series = []
    for (pid in data_map) {
        var c = genColorByPid(pid)
        var ss = {
            name: pid,
            type: 'line',
            smooth: true,
            symbol: 'none',
            showSymbol: false,
            sampling: 'average',
            itemStyle: {
                color: c
            },
            areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: c
                }, {
                    offset: 1,
                    color: '#ffe'
                }])
            },
            data: data_map[pid]
        }
        series.push(ss)
    }
    return series
}

