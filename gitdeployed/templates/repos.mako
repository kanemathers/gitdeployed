<div class="container">
    <div class="page-header">
        <button class="pull-right btn btn-primary" data-bs-modal="'partials/new-repo.html'" data-ng-controller="ReposCtrl">New Repo</button>

        <h1>Repositories</h1>
    </div>

    <div data-ng-show="!repos.length">
        <p>No repositories.</p>
    </div>

    <div class="row">
        <div class="span3">
            <div class="tabs-left">
                <ul class="nav nav-tabs">
                    <li data-ng-repeat="repo in repos">
                        <a>{{repo.path}}</a>
                    </li>
                </ul>
            </div>
        </div>
        <div class="span9">
        </div>
    </div>
</div>
