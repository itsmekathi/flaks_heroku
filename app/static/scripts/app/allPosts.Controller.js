(function () {
    'use strict';
    angular.module('app')
        .controller('allPostsController', ['$scope', '$http', '$log', function ($scope, $http, $log) {
            $scope.method = 'GET';
            $scope.posts_url = '/api/v1/posts';
            $scope.status = '';
            $scope.posts = [];

            $scope.get_all_posts = function () {
                $scope.posts = [];
                $http({
                    method: $scope.method,
                    url: $scope.posts_url
                }).then(function (response) {
                    $scope.status = response.status;
                    $scope.posts = response.data.posts;

                }, function (response) {
                    $scope.data = response.data.posts || 'Request failed';
                    $scope.status = response.status;
                });
            };

            $scope.get_all_posts();
        }]);
})();