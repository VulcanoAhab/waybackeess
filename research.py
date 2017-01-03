
def run_archive(site_url, report_name, dateess_obj):
    '''
    '''
    arquive=Snap(site_url, report_name, dateess_obj)
    arquive.map_availables()
    arquive.save_availables()

if __name__ == '__main__':
    import json
    import argparse
    from snapshots import Snap
    from date import way_date
    from date import Dateess

    parser = argparse.ArgumentParser(
                        description='Fetch and analyse Internet Archive\
                                    websites\' snapshots')

    parser.add_argument('--url', '-u')
    parser.add_argument('--report', '-r', default='sites')
    parser.add_argument('--date_start', '-s', help='Date format YYYMMDD')
    parser.add_argument('--date_end', '-e', help='Date format YYYMMDD')
    parser.add_argument('--config', '-c', default='config.json')

    args = parser.parse_args()

    if args.url:
        if not args.date_start or not args.date_end:
            raise Exception('[-] Date range is required on command line')
        date_start=way_date(args.date_start)
        date_end=way_date(args.date_end)
        dss=Dateess()
        dss.start_year=date_start.year
        dss.start_month=date_start.month
        dss.start_day=date_start.day
        dss.end_year=date_end.year
        dss.end_month=date_end.month
        dss.end_day=date_end.day
        run_archive(args.url, args.report, dss)
    else:
        config_file=open(args.config)
        configs=json.load(config_file)
        config_file.close()
        for site,config in configs.items():
            report_name=config.pop('report')
            dss=Dateess.load(config)
            run_archive(site,report_name,dss)
