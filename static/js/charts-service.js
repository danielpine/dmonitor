var chart_store = {};

function render(id, xdata, series, title, callback) {
  option = {
    grid: {
      // bottom: "0px",
      top: "30px",
      left: "60px",
      right: "30px",
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
        snap: true,
        label: {
          margin: 50,
        },
      },
      formatter: (params) => {
        params.sort(function (a, b) {
          return b.data[1] - a.data[1];
        });
        var d = [];
        d.push(formatdate(params[0].axisValue));
        d.push('<table style="width:100%;">');
        params.forEach((e) => {
          d.push('<tr style="height:5px;line-height:10px">');
          d.push(
            '<td width:10px;><span class=rect style="background-color:' +
              e.color +
              ';"></span></td><td style="text-align:left;">' +
              e.seriesName +
              ':</td><td style="text-align:right;">' +
              e.data[1] +
              "</td>"
          );
          d.push("</tr>");
        });
        d.push("</table>");
        return d.join("");
      },
    },
    title: {
      left: "center",
      text: title,
    },
    legend: {
      type: "scroll",
      selectedMode: "multiple",
      icon: "path://M19,11H5a1,1,0,0,0,0,2H19a1,1,0,0,0,0-2Z",
      selector: ["all", "inverse"],
      left: "left",
      align: "left",
      bottom: 0,
      orient: "horizontal",
    },
    toolbox: {
      feature: {
        dataZoom: {
          yAxisIndex: "none",
        },
        restore: {},
        saveAsImage: {},
      },
    },
    xAxis: {
      type: "time",
      min: "dataMin",
      max: "dataMax",
      minInterval: 1,
      maxInterval: 3600 * 24 * 1000,
      boundaryGap: ["20%", "20%"],
      interval: 10 * 1000,
      // data: xdata,
      axisLabel: {
        formatter: function (value, index) {
          // return formatdate(value);
          return echarts.format.formatTime("hh:mm:ss", value);
        },
      },
      axisPointer: {
        lineStyle: {
          color: "#004E52",
          opacity: 0.5,
          width: 2,
        },
        label: {
          show: true,
          formatter: function (params) {
            return echarts.format.formatTime(
              "yyyy-MM-dd hh:mm:ss",
              params.value
            );
          },
          backgroundColor: "#004E52",
        },
      },
    },
    yAxis: {
      type: "value",
      boundaryGap: [0, "100%"],
    },
    dataZoom: [
      {
        type: "inside",
        throttle: 50,
      },
    ],
    series: series,
  };
  if (!chart_store[id]) {
    chart_store[id] = echarts.init(document.getElementById(id), null, {
      // renderer: 'svg',
    });
  }
  chart_store[id].setOption(option, typeof callback == "boolean" && callback);
}
var resizeDebounce = null;
window.addEventListener("resize", function () {
  function resizePlot() {
    Object.values(chart_store).forEach((chart) => chart.resize());
  }
  if (resizeDebounce) {
    window.clearTimeout(resizeDebounce);
  }
  resizeDebounce = window.setTimeout(resizePlot, 100);
});

function pushData(map, pid, t, val) {
  if (!map[pid]) {
    map[pid] = [];
  }
  map[pid].push([t, val]);
}

function rgb2hex(item) {
  if (item && item.length == 3) {
    var a = item[0],
      b = item[1],
      c = item[2],
      d = "#",
      cArray = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
      ];
    d += cArray[Math.floor(a / 16)] + "" + cArray[a % 16] + "";
    d += cArray[Math.floor(b / 16)] + "" + cArray[b % 16] + "";
    d += cArray[Math.floor(c / 16)] + "" + cArray[c % 16] + "";
    return d;
  }
}

function genSeries(data_map) {
  var series = [];
  for (pid in data_map) {
    var rgb = colorHash.rgb(pid);
    var color = rgb2hex(rgb);
    series.push({
      name: pid,
      type: "line",
      smooth: true,
      symbol: "none",
      showSymbol: false,
      sampling: "average",
      itemStyle: {
        color: color,
      },
      lineStyle: {
        width: 1,
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: "rgba(" + rgb[0] + "," + rgb[1] + ", " + rgb[2] + ", 0.1)",
          },
        ]),
      },
      data: data_map[pid],
    });
  }
  return series;
}
