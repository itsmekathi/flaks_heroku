(function () {
    'use strict';

    angular.module('app')
        .controller('WordcountController', ['$scope', '$log', function ($scope, $log) {
            $scope.getResults = function () {
                $log.log('test');
            };
        }]);
})();