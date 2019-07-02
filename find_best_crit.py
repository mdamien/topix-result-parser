n_clusters = 2
n_clusters_max = 5
n_clusters2 = 2
n_clusters2_max = 5
n_topics = 2
n_topics_max = 5
n_repeat = 25
run_dir = "example/"

###############################################

groups = {}
for q in range(n_clusters, n_clusters_max + 1):
    for k in range(n_topics, n_topics_max + 1):
        for l in range(n_clusters2, n_clusters2_max + 1):
            groups['%d,%d,%d' % (k, q, l)] = {}

if len(groups.keys()) == 0:
    print('ERROR: NO (?,?) RESULTS FOUND')

max_clusters = 0
for group, group_result in groups.items():
    best_result = None
    best_crit = None
    for rep in range(n_repeat):
        result = {}
        group_run_prefix = run_dir + 'out/' + str(rep)

        n_topics, n_clusters, n_clusters2 = [int(x) for x in group.split(',')]
        result['n_topics'] = n_topics
        result['n_clusters'] = n_clusters
        result['n_clusters2'] = n_clusters2
        result['n_repeat'] = rep
        print()
        print(result)
        try:
            clusters = open(group_run_prefix + 'cluster(%s)' % group).read()
        except FileNotFoundError:
            print('ERROR: NO CLUSTERS FOR %s' % group)
            print(group_run_prefix + 'cluster(%s)' % group)
            clusters = ''
        print('clusters:', len(clusters), clusters)
        max_clusters = max(len(clusters), max_clusters)
        result['clusters'] = clusters

        try:
            topics = open(group_run_prefix + 'beta(%s)' % group).read()
        except FileNotFoundError:
            print('ERROR: NO TOPICS FOR %s - beta' % group)
            topics = ''
        result['topics'] = topics

        try:
            topics_per_edges = open(group_run_prefix + 'phi_sum(%s)' % group).read()
        except FileNotFoundError:
            print('ERROR: NO topics_per_edges FOR %s - phi_sum' % group)
            topics_per_edges = ''
        result['topics_per_edges'] = topics_per_edges

        try:
            rho_mat = open(group_run_prefix + 'rho(%s)' % group).read()
        except FileNotFoundError:
            print('ERROR: NO rho_mat FOR %s - rho' % group)
            rho_mat = ''
        result['rho_mat'] = rho_mat

        try:
            pi_mat = open(group_run_prefix + 'Pi(%s)' % group).read()
        except FileNotFoundError:
            print('ERROR: NO pi_mat FOR %s - PI' % group)
            pi_mat = ''
        result['pi_mat'] = pi_mat

        try:
            theta_qr_mat = open(group_run_prefix + 'thetaQR(%s)' % group).read()
        except FileNotFoundError:
            print('ERROR: NO thetaQR FOR %s' % group)
            theta_qr_mat = ''
        result['theta_qr_mat'] = theta_qr_mat

        try:
            crit = float(open(group_run_prefix + 'crit(%s)' % group).read())
        except FileNotFoundError:
            print('ERROR: NO CRIT FOR %s' % group)
            crit = None
        result['crit'] = crit

        if not best_crit or (crit and crit > best_crit):
            best_result = result
            best_crit = crit

    for key in best_result:
        group_result[key] = best_result[key]

results = sorted(list(groups.items()), key=lambda x: x[1]['crit'])

key, group_result = results[-1]

print("best:", key)
print('  > topics:', group_result['n_topics'])
print('  > len(topics):', len(group_result['topics']))
print('  > clusters:', group_result['n_clusters'])
print('  > len(clusters):', len(group_result['clusters']))
print('  > clusters2:', group_result['n_clusters2'])
print('  > n_repeat:', group_result['n_repeat'])
print('  > crit:', group_result['crit'])