import click

import coiled


def find_cluster(cloud: coiled.Cloud, cluster: str):
    if cluster and cluster.isnumeric():
        cluster_id = int(cluster)
    elif cluster:
        # get cluster by name
        try:
            clusters = cloud.get_clusters_by_name(name=cluster)
            if clusters:
                recent_cluster = clusters[-1]
            else:
                raise click.ClickException(
                    f"Unable to find cluster with name '{cluster}' in account '{cloud.default_account}'"
                )

            cluster_id = recent_cluster["id"]

        except coiled.errors.DoesNotExist:
            cluster_id = None
    else:
        # default to most recent cluster
        clusters = cloud.list_clusters(max_pages=1)
        if not clusters:
            raise ValueError(f"Unable to find any clusters for account '{cloud.default_account}'")
        match = max(clusters, key=lambda c: c["id"])
        cluster_id = match["id"]

    if not cluster_id:
        raise click.ClickException(f"Unable to find cluster `{cluster}`")

    try:
        cluster_info = cloud.cluster_details(cluster_id)
    except coiled.errors.ServerError as e:
        if "not found" in str(e).lower():
            raise click.ClickException(f"Unable to find cluster with id {cluster_id}") from None
        else:
            raise e

    return cluster_info
