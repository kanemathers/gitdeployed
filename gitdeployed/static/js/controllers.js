angular.module('gitdeployed.controllers', [
    'gitdeployed.services'
])

.controller('ReposCtrl', [
    '$scope',
    'Repos',

    function($scope, Repos)
    {
        Repos.query(function(repos)
        {
            $scope.repos = repos;
        });

        $scope.addRepo = function(fn)
        {
            if (!this.path || !this.upstream)
                return false;

            var repo = new Repos({
                path:     this.path,
                upstream: this.upstream
            });

            repo.$save();
            fn();
        };
    }
]);
