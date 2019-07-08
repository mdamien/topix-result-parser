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
        #print()
        #print(result)

        try:
            Cclusters = open(group_run_prefix + 'Ccluster(%s)' % group).read().strip()
        except FileNotFoundError:
            print('ERROR: NO C-CLUSTERS FOR %s' % group)
            continue
            Cclusters = ''
        #print('Cclusters:', len(Cclusters), Cclusters)
        result['Cclusters'] = Cclusters

        try:
            Rclusters = open(group_run_prefix + 'Rcluster(%s)' % group).read().strip()
        except FileNotFoundError:
            print('ERROR: NO R-CLUSTERS FOR %s' % group)
            continue
            Rclusters = ''
        #print('Rclusters:', len(Rclusters), Rclusters)
        result['Rclusters'] = Rclusters

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

    if not best_result: continue
    for key in best_result:
        group_result[key] = best_result[key]

results = sorted([(k, g) for k, g in groups.items() if g], key=lambda x: x[1]['crit'])

for i in (-1,): #(-1, -2, -3):
    key, group_result = results[i]

    print()
    print('###################################')
    print("best %s:" % i, key)
    print('  > topics:', group_result['n_topics'])
    print('  > len(topics):', len(group_result['topics']))
    print('  > Cclusters:', group_result['n_clusters'])
    print('       >', group_result['Cclusters'])
    print('  > Rclusters:', group_result['n_clusters2'])
    print('       >', group_result['Rclusters'])
    print('  > n_repeat:', group_result['n_repeat'])
    print('  > crit:', group_result['crit'])
    print(' --# ', group_result['n_repeat'], 'Ccluster(', key, ')', sep='')