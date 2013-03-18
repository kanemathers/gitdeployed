angular.module('gitdeployed.controllers', [
    'gitdeployed.services'
])

.controller('LoginCtrl', [
    '$scope',
    '$http',

    function($scope, $http)
    {
        $scope.authed = true;

        $scope.login = function()
        {
            $http.post('/login', {
                username: this.username,
                password: this.password
            })
            .success(function(user)
            {
                $scope.authed = true;
                $scope.error  = '';

                $scope.$emit('auth:success', user);
            })
            .error(function(resp)
            {
                $scope.error = resp;
            });
        };

        $scope.$on('auth:required', function()
        {
            $scope.authed = false;
        });
    }
])

.controller('ReposListCtrl', [
    '$scope',
    'Repos',

    function($scope, Repos)
    {
        $scope.setActive = function(repo)
        {
            $scope.activeRepo = repo;
        };

        $scope.deleteRepo = function(repo)
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

                $scope.setActive($scope.repos[0]);
            });

            $scope.activeRepo = null;
        };

        $scope.$on('repos.new', function(event, repo)
        {
            $scope.repos.push(repo);
            $scope.setActive(repo);
        });

        Repos.query(function(repos)
        {
            $scope.repos = repos;

            $scope.setActive(repos[0]);
        });
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
                $scope.error = null;

                $scope.$emit('repos.new', resp);
                fn();
            },
            function(resp)
            {
                $scope.error = resp.data;
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
