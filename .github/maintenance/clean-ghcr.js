import pkg from '@octokit/core';

const {Octokit} = pkg;

const args = process.argv.slice(2);
const org = args[0]
const package_name = args[1]
const minNumToKeep = args[2]
const package_type = 'container'

console.log('Process container ' + package_name + '@' + org + ', will keep ' + minNumToKeep + ' versions')

const octokit = new Octokit(
    {auth: process.env.GITHUB_ACCESS_TOKEN}
)

async function getAllVersions() {
    return await octokit.request('GET /orgs/{org}/packages/{package_type}/{package_name}/versions', {
        package_type: package_type,
        package_name: package_name,
        org: org
    }).catch(console.error)
}

async function deleteVersion(package_version_id) {
    return await octokit.request('DELETE /orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id}', {
        package_type: package_type,
        package_name: package_name,
        org: org,
        package_version_id: package_version_id
    }).catch(console.error)
}

async function deleteVersions(toDelete) {
    await Promise.allSettled(toDelete.map(pkg_id => deleteVersion(pkg_id)))
}

getAllVersions().then((response) => {

    const untaggedVersions = response.data.filter(pkg => pkg.metadata.container.tags.length < 1).map(pkg => pkg.id);
    console.log('There are ' + untaggedVersions.length + ' untagged versions')

    const versionsToDelete = untaggedVersions.slice(minNumToKeep)
    console.log('We keep ' + minNumToKeep + ' versions, so we should delete ' + versionsToDelete.length + ' versions')

    deleteVersions(versionsToDelete).then(() => {
        console.log('Sent all requests to GitHub!')
    })
})
