import shutil
import os
from git import Repo, Git, config, GitCommandError

my_account = os.environ.get('GITHUB_USERNAME', None)

def push_to_github(local_dir, repo_path, commit_message='No commit message was set.', github_username=os.environ.get('GITHUB_USERNAME', None), github_password=os.environ.get('GITHUB_PASSWORD', None)):
    local_dir = local_dir.split('/')[0]
    repo_list = repo_path.split('/')
    try:
        n = repo_list.index('tree')
    except ValueError:
        n = len(repo_list)
    repo_name = os.path.join(*repo_list[:n])
    repo_url = '/'.join(['https://' + github_username + ':' + github_password + '@github.com',github_username,repo_name])
    branch = repo_list[-1] if 'tree' in repo_list else None

    os.system('cd')
    git_dir = os.path.join('dest_repo', repo_name)
    try:
        shutil.rmtree(git_dir)
        shutil.rmtree('dest_repo')
    except:
        pass
    os.system('md dest_repo')
    kwargs = { 'url': repo_url, 'to_path': git_dir }
    if branch:
        kwargs['branch'] = branch
    repo = Repo.clone_from(**kwargs)
    os.chdir(git_dir)
    os.system('find . | grep -v "git" | xargs rm -rf')
    print('local_dir', local_dir)
    os.system(' '.join(['cp', '-rf', os.path.join('..', '..', local_dir, '.'), '.']))

    origin = repo.remotes[0]

    gitcmd = Git('.')
    gitcmd.config('--add', 'user.name', os.environ.get('GITHUB_USERNAME', None))
    gitcmd.config('--add', 'user.email', os.environ.get('GITHUB_EMAIL', None))
    gitcmd.config('--add', 'core.autocrlf', 'true')
    #repo.index.remove(["*"])
    repo.git.add(u=True)
    repo.git.add(A=True)
    repo.index.commit(commit_message)
    repo.git.push('--set-upstream', 'origin', branch)
    stats = repo.head.commit.stats.total

    os.chdir('../..')
    shutil.rmtree('dest_repo')
    return stats

def clone_from_github(repo_name,account=my_account,github_username=os.environ.get('GITHUB_USERNAME', None), github_password=os.environ.get('GITHUB_PASSWORD', None)):
    local_dir = repo_name
    repo_url = '/'.join(['https://' + github_username + ':' + github_password + '@github.com',account,repo_name])
    if os.path.exists(local_dir):
        shutil.rmtree(local_dir)
    try:
        repo = Repo.clone_from(repo_url,local_dir)
    except GitCommandError as e:
        None

def copy_from_github(repo_name,account=my_account,github_username=os.environ.get('GITHUB_USERNAME', None), github_password=os.environ.get('GITHUB_PASSWORD', None)):
    repo_list = repo_name.split('/')
    repo_name = repo_list[0]
    branch = repo_list[-1] if 'tree' in repo_list else None
    repo_url = '/'.join(['https://' + github_username + ':' + github_password + '@github.com',account,repo_name])
    repo = Repo.clone_from(repo_url,'_temp')
    if branch:
        repo.git.checkout(branch)
    shutil.rmtree('_temp/.git')
    os.system('cp -r {} {}'.format('_temp/.', repo_name))
    shutil.rmtree('_temp')
    return { 'file_count': len(os.listdir(repo_name)) }