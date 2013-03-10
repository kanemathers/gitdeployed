angular.module('gitdeployed.controllers', [
    'gitdeployed.services'
])

.controller('ReposListCtrl', [
    '$scope',
    'Repos',

    function($scope, Repos)
    {
        Repos.query(function(repos)
        {
            $scope.repos = repos;

            $scope.setActive(repos[0]);
        });

        $scope.setActive = function(repo)
        {
            $scope.activeRepo = repo;
        };

        $scope.delete = function(repo)
        {
            repo.$delete(function()
            {
                for (var i = 0; i < $scope.repos.length; i++)
                {
                    if ($scope.repos[i].id != repo.id)
                        continue;

                    $scope.repos.splice(i, 1);

                    break;
                };

                // TODO: select and set a new activeRepo
            });
        };
    }
])

.controller('ReposNewCtrl', [
    '$scope',
    'Repos',

    function($scope, Repos)
    {
        $scope.addRepo = function(fn)
        {
            if (!this.upstream)
                return false;

            var repo = new Repos({
                path:     this.path || null,
                upstream: this.upstream
            });

            repo.$save(function(resp)
            {
                // TODO: need to push this to ``ReposListCtrl.repos`` and
                // set it as active
                fn();
            });
        };
    }
])

.controller('ConfigCtrl', [
    '$scope',

    function($scope)
    {
        
    }
]);
