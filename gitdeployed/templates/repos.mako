<div class="container">
    <div class="page-header">
        <button class="pull-right btn btn-primary" data-bs-modal="'partials/new-repo.html'" data-ng-controller="ReposCtrl">Add Repo</button>

        <h1>Repositories</h1>
    </div>

    <div data-ng-show="!repos.length">
        <p>No repositories.</p>
    </div>

    <div class="tabbable tabs-left">
        <ul class="nav nav-tabs">
            <li data-ng-repeat="repo in repos | orderBy: 'path'" data-ng-class="{active: repo.id == activeRepo.id}">
                <a data-ng-click="setActive(repo)">{{repo.path}}</a>
            </li>
        </ul>

        <div class="tab-content" data-ng-show="activeRepo">
            <div class="alert alert-info">
                <i class="icon-cog icon-white"></i> Set your POST service hook to post to <strong><a data-ng-href="{{'${request.application_url}' + '/repos/' + activeRepo.id + '/sync'}}">{{'${request.application_url}' + '/repos/' + activeRepo.id + '/sync'}}</a></strong>
            </div>

            <dl class="dl-horizontal">
                <dt>POST Hook</dt>
                <dd>{{'${request.application_url}' + '/repos/' + activeRepo.id + '/sync'}}</dd>
                <dt>Path</dt>
                <dd>{{activeRepo.path}}</dd>
                <dt>Upstream</dt>
                <dd>{{activeRepo.upstream}}</dd>
            </dl>
        </div>
    </div>
</div>
