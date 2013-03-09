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
            if (!this.upstream)
                return false;

            var repo = new Repos({
                path:     this.path || null,
                upstream: this.upstream
            });

            repo.$save();
            fn();
        };
    }
]);
