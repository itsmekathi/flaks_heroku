(function () {
    'use strict';
    angular.module('app', ['ngMaterial', 'ngMessages', 'chart.js',
        'ui.grid', 'ngTouch', 'ui.grid.edit', 'ui.grid.rowEdit', 'ui.grid.cellNav']);
    angular.module('app')
        .config(["ChartJsProvider", function (ChartJsProvider) {
            ChartJsProvider.setOptions({
                chartColors: ['#803690', '#00ADF9', '#DCDCDC',
                    '#46BFBD', '#FDB45C', '#949FB1', '#4D5360']
            });
        }]);
})();