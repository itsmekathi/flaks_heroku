(function () {
    'use strict';
    angular.module('app')
        .controller('todoListDetailsChartController', ['$scope', '$http', '$log', function ($scope, $http, $log) {
            $log.log('Todo List details chart controller initialized');
            $scope.method = 'GET';
            $scope.baseUrl = '/api/v1/todo_list/';
            $scope.todoListId = parseInt($('#todoListIdInput')[0].value);
            $scope.chartData = {};

            $scope.options = {
                responsive: true,
                legend: {
                    display: true,
                    position: 'right',
                },
                title: {
                    display: true,
                    text: 'To-do list chart view',
                    position: 'top'
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            };
            $scope.getDataForChart = function () {
                $http({
                    method: $scope.method,
                    url: $scope.baseUrl + $scope.todoListId + '/chart'
                }).then(function (response) {
                    $log.log('Successfully fetched data');
                    $scope.chartData = response.data.chartData;
                }, function (response) {
                    $scope.status = response.status;
                    $log.log('Failed fetching data');
                });
            };
            $scope.getDataForChart();
        }]);
})();