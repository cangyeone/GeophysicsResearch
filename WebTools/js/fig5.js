    var myChart5 = echarts.init(document.getElementById('figure5'));
$.getJSON('js/data-1491900403342-rkjxOfqTl.json', function (buildingsGeoJSON) {

    echarts.registerMap('buildings', buildingsGeoJSON);

    var regions = buildingsGeoJSON.features.map(function (feature) {
        return {
            name: feature.properties.name,
            value: Math.max(Math.sqrt(feature.properties.height), 0.1),
            height: Math.max(Math.sqrt(feature.properties.height), 0.1)
        };
    });
    
    
    myChart5.setOption({
        visualMap: {
            show: false,
            min: 0.4,
            max: 8,
            inRange: {
                color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
            }
        },
        series: [{
            type: 'map3D',
            map: 'buildings',
            shading: 'realistic',
            realisticMaterial: {
                roughness: 0.6,
                textureTiling: 20
            },
            postEffect: {
                enable: true,
                bloom: {
                    enable: false
                },
                SSAO: {
                    enable: true,
                    quality: 'medium',
                    radius: 10,
                    intensity: 1.2
                },
                depthOfField: {
                    enable: false,
                    focalRange: 5,
                    fstop: 1,
                    blurRadius: 6
                }
            },
            groundPlane: {
                show: true,
                color: '#333'
            },
            light: {
                main: {
                    intensity: 6,
                    shadow: true,
                    shadowQuality: 'high',
                    alpha: 30
                },
                ambient: {
                    intensity: 0
                },
                ambientCubemap: {
                    texture: 'js/data-1491896094618-H1DmP-5px.hdr',
                    exposure: 2,
                    diffuseIntensity: 1,
                    specularIntensity: 1
                }
            },
            viewControl: {
                minBeta: -360,
                maxBeta: 360
            },

            itemStyle: {
                areaColor: '#666'
                // borderColor: '#222',
                // borderWidth: 1
            },

            label: {
                textStyle: {
                    color: 'white'
                }
            },

            silent: true,

            instancing: true,

            boxWidth: 200,
            boxHeight: 1,

            data: regions
        }]
    });

});

