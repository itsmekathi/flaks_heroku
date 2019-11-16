(function () {
    'use strict';
    angular.module('app', ['ngMaterial', 'ngMessages', 'chart.js']);
    angular.module('app')
        .config(["ChartJsProvider", function (ChartJsProvider) {
            ChartJsProvider.setOptions({ chartColors: ['#803690', '#00ADF9', '#DCDCDC', '#46BFBD', '#FDB45C', '#949FB1', '#4D5360'] });
        }]);
})();