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

        $scope.addRepo = function(name, description, path, upstream)
        {
            var repo = new Repos({
                name:        name,
                description: description,
                path:        path,
                upstream:    upstream
            });

            repo.$save();
        };

        //$scope.addRepo('asda', 'my test repo', '/dev/repo', 'git@asdsa.com/asd');
    }
]);
