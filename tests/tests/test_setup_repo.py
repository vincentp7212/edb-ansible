import pytest

from conftest import (
    load_ansible_vars,
    get_hosts,
    get_os,
    get_pg_type,
    get_primary,
    EDB_ENABLE_REPO,
)

def test_setup_repo_edb_centos():
    if not EDB_ENABLE_REPO:
        pytest.skip()

    if not get_os().startswith('centos') and not get_os().startswith('rocky'):
        pytest.skip()

    host = get_primary()
    cmd = host.run("yum repolist")
    assert cmd.succeeded, \
        "Unable to list the package repository list"
    assert "EnterpriseDB RPMs" in cmd.stdout, \
        "Access to the EDB package repository not configured"

def test_setup_repo_pgdg_centos():
    if not get_os().startswith('centos') and not get_os().startswith('rocky'):
        pytest.skip()

    if get_pg_type() != 'PG':
        pytest.skip()

    host = get_primary()
    cmd = host.run("yum repolist")
    assert cmd.succeeded, \
        "Unable to list the package repository list on %s" % host
    assert "PostgreSQL common RPMs for RHEL / Rocky 8" in cmd.stdout, \
        "Access to the PGDG package repository not configured"

def test_setup_repo_edb_debian():
    if not EDB_ENABLE_REPO:
        pytest.skip()

    if not (get_os().startswith('debian') or get_os().startswith('ubuntu')):
        pytest.skip()

    host = get_primary()
    cmd = host.run("grep -rhE ^deb /etc/apt/sources.list*")
    assert cmd.succeeded, \
        "Unable to list the package repository list"
    assert "apt.enterprisedb.com" in cmd.stdout, \
        "Access to the EDB package repository not configured"

def test_setup_repo_pgdg_debian():
    if not (get_os().startswith('debian') or get_os().startswith('ubuntu')):
        pytest.skip()

    if get_pg_type() != 'PG':
        pytest.skip()

    host = get_primary()
    cmd = host.run("grep -rhE ^deb /etc/apt/sources.list*")
    assert cmd.succeeded, \
        "Unable to list the package repository list"
    assert "apt.postgresql.org" in cmd.stdout, \
        "Access to the PGDG package repository not configured"
