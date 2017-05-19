    var myChart6 = echarts.init(document.getElementById('figure6'));
    option6 = {
    series: []
};

var zr = myChart6.getZr();

var average_fps = [];
var fpsValue = 0;

var circles = [];
var data = [];

var numEl = new echarts.graphic.Text({
    style: {
        text: '',
        font: '40px Helvetica',
        textAlign: 'left',
        textBaseline: 'top'
    },
    position: [10, 10]
});

var fpsEl = new echarts.graphic.Text({
    style: {
        text: 0,
        font: '40px Helvetica',
        textAlign: 'left',
        textBaseline: 'top'
    },
    position: [10, 60]
});
zr.add(numEl);
zr.add(fpsEl);

function mapX(val) {
    return (val + 5) / 10 * zr.getWidth();
}

function mapY(val) {
    return (val + 5) / 10 * zr.getHeight();
}

time0 = Date.now();

zr.animation.on('frame', function() {


    if (fpsValue > 24) {
        for (var g = 0; g < 10; g++) {
            data.push({
                xloc: 0,
                yloc: 0,
                xvel: 0,
                yvel: 0
            });

            var circle = new echarts.graphic.Rect({
                shape: {
                    x: 10,
                    y: 10
                },
                style: {
                    fill: 'red'
                }
            });
            circles.push(circle);
            zr.add(circle);
        }

        numEl.setStyle('text', data.length);
    }

    data.forEach(function(d, idx) {
        d.xloc += d.xvel;
        d.yloc += d.yvel;
        d.xvel += 0.04 * (Math.random() - .5) - 0.05 * d.xvel - 0.0005 * d.xloc;
        d.yvel += 0.04 * (Math.random() - .5) - 0.05 * d.yvel - 0.0005 * d.yloc;
        var size = Math.min(1 + 1000 * Math.abs(d.xvel * d.yvel), 10);
        circles[idx].setShape('width', size);
        circles[idx].setShape('height', size);
        circles[idx].position = [mapX(d.xloc), mapY(d.yloc)];
    });


    time1 = Date.now();

    var currentFPS = Math.round(1000 / (time1 - time0));
    if (!isNaN(currentFPS)) {
        average_fps.push(currentFPS);
        if (average_fps.length === 10) {
            var avg = 0;
            for (var h = 0; h < average_fps.length; h++) {
                avg += average_fps[h];
            }
            fpsValue = avg / average_fps.length;
            fpsEl.setStyle('text', fpsValue);
            average_fps = [];
        }
    }
    time0 = time1;
});
 myChart6.setOption(option6);