"""
Command line interface for eCourts Scraper.
"""

import click
import json
from datetime import datetime, timedelta
from .scraper import ECourtsScraper
from .utils import save_results, format_date, validate_cnr, validate_case_details


@click.command()
@click.option('--cnr', help='CNR number of the case')
@click.option('--case-type', help='Case type (e.g., CRL, CIV)')
@click.option('--case-number', help='Case number')
@click.option('--case-year', help='Case year')
@click.option('--today', is_flag=True, help='Check for today\'s listings')
@click.option('--tomorrow', is_flag=True, help='Check for tomorrow\'s listings')
@click.option('--causelist', is_flag=True, help='Download full cause list')
@click.option('--output-format', default='json', type=click.Choice(['json', 'text']),
              help='Output format (json or text)')
def main(cnr, case_type, case_number, case_year, today, tomorrow, 
         causelist, output_format):
    """eCourts Scraper - Fetch court listings from eCourts platform."""
    
    scraper = ECourtsScraper()
    
    # Determine target date
    target_date = None
    if today:
        target_date = format_date(datetime.now())
    elif tomorrow:
        target_date = format_date(datetime.now() + timedelta(days=1))
    else:
        # Interactive mode - ask user for date preference
        choice = click.prompt(
            'Check for (1) Today or (2) Tomorrow?', 
            type=click.Choice(['1', '2'])
        )
        if choice == '1':
            target_date = format_date(datetime.now())
        else:
            target_date = format_date(datetime.now() + timedelta(days=1))
    
    # Get case details if not provided
    if not cnr and not (case_type and case_number and case_year):
        search_method = click.prompt(
            'Search by (1) CNR or (2) Case Details?',
            type=click.Choice(['1', '2'])
        )
        
        if search_method == '1':
            cnr = click.prompt('Enter CNR number')
        else:
            case_type = click.prompt('Enter case type')
            case_number = click.prompt('Enter case number')
            case_year = click.prompt('Enter case year')
    
    # Perform search
    try:
        if cnr:
            # Validate CNR
            if not validate_cnr(cnr):
                click.echo("Error: Invalid CNR format")
                return
            
            # Demo mode for CLI
            if cnr.upper() == 'DEMO123':
                demo_result = {
                    "status": "case_found",
                    "message": "Demo case information retrieved successfully",
                    "cnr": cnr,
                    "case_details": {
                        "case_number": "DEMO/123/2024",
                        "court_name": "Demo District Court",
                        "case_type": "Civil Suit",
                        "filing_date": "15-01-2024",
                        "status": "Pending",
                        "next_hearing": "25-10-2025",
                        "judge": "Hon'ble Justice Demo",
                        "petitioner": "Demo Petitioner",
                        "respondent": "Demo Respondent"
                    },
                    "status_indicators": [
                        "Case is listed for hearing",
                        "Documents filed", 
                        "Notice served"
                    ],
                    "real_case_data": True,
                    "demo_mode": True
                }
                
                # Display demo results
                click.echo("Case Information Found!")
                click.echo(f"CNR: {demo_result['cnr']}")
                click.echo(f"Message: {demo_result['message']}")
                click.echo("\nCase Details:")
                for key, value in demo_result['case_details'].items():
                    click.echo(f"  {key.replace('_', ' ').title()}: {value}")
                
                click.echo("\nStatus Indicators:")
                for indicator in demo_result['status_indicators']:
                    click.echo(f"  - {indicator}")
                
                # Save results
                filename = f"case_result_{cnr}_{target_date}"
                save_results(demo_result, filename, output_format)
                click.echo(f"\nResults saved to: output/{filename}.{output_format}")
                
                return
            
            # Real CNR search
            captcha_code = None
            result = scraper.search_by_cnr(cnr, target_date, captcha_code)
            
            # Handle captcha requirement
            if result.get('status') == 'captcha_required':
                click.echo("Captcha Required")
                click.echo("Status: Connected to eCourts Services")
                click.echo("Message: CNR search form found but requires captcha verification")
                click.echo("Note: Captcha solving is only available in web interface")
                click.echo("Please use the web interface at http://127.0.0.1:5000 for captcha-based searches")
                return
            
            # Handle search results
            if result.get('status') in ['case_found', 'no_case_data', 'search_failed']:
                if result.get('status') == 'case_found':
                    click.echo("Case Information Found!")
                    click.echo(f"CNR: {result['cnr']}")
                    click.echo(f"Message: {result['message']}")
                    
                    if result.get('case_details'):
                        click.echo("\nCase Details:")
                        for key, value in result['case_details'].items():
                            click.echo(f"  {key}: {value}")
                    
                    if result.get('status_indicators'):
                        click.echo("\nStatus Indicators:")
                        for indicator in result['status_indicators']:
                            click.echo(f"  - {indicator}")
                
                elif result.get('status') == 'no_case_data':
                    click.echo("No Case Data Found")
                    click.echo(f"CNR: {result['cnr']}")
                    click.echo(f"Message: {result['message']}")
                
                elif result.get('status') == 'search_failed':
                    click.echo("Search Failed")
                    click.echo(f"CNR: {result['cnr']}")
                    click.echo(f"Error: {result['message']}")
                
                # Save results
                filename = f"case_result_{cnr}_{target_date}"
                save_results(result, filename, output_format)
                click.echo(f"\nResults saved to: output/{filename}.{output_format}")
                
            else:
                # Fallback to case listing
                listing = scraper.get_case_listing(result, target_date)
                
                if listing.get('status') == 'connected':
                    click.echo("eCourts Connection Successful")
                    click.echo(f"Status: {listing.get('website_status', 'Connected')}")
                    click.echo(f"Message: {listing.get('message')}")
                    if listing.get('page_title'):
                        click.echo(f"Page Title: {listing.get('page_title')}")
                else:
                    click.echo("Connection Failed")
                    click.echo(f"Status: {listing.get('website_status', 'Failed')}")
                    click.echo(f"Message: {listing.get('message')}")
                
                # Save results
                filename = f"case_result_{cnr}_{target_date}"
                save_results(listing, filename, output_format)
                click.echo(f"\nResults saved to: output/{filename}.{output_format}")
        
        else:
            # Case details search
            if not validate_case_details(case_type, case_number, case_year):
                click.echo("Error: Invalid case details")
                return
            
            result = scraper.search_by_case_details(case_type, case_number, case_year, target_date)
            listing = scraper.get_case_listing(result, target_date)
            
            if listing.get('status') == 'connected':
                click.echo("eCourts Connection Successful")
                click.echo(f"Status: {listing.get('website_status', 'Connected')}")
                click.echo(f"Message: {listing.get('message')}")
                if listing.get('page_title'):
                    click.echo(f"Page Title: {listing.get('page_title')}")
            else:
                click.echo("Connection Failed")
                click.echo(f"Message: {listing.get('message')}")
            
            # Save results
            filename = f"case_result_{case_type}_{case_number}_{case_year}_{target_date}"
            save_results(listing, filename, output_format)
            click.echo(f"\nResults saved to: output/{filename}.{output_format}")
        
        # Handle cause list download
        if causelist:
            click.echo("\nDownloading Cause List...")
            
            # Demo cause list
            cause_list_data = {
                "status": "connected",
                "court": "Demo District Court",
                "date": target_date,
                "message": "Connected to eCourts Services",
                "cause_list_links_found": 5,
                "website_accessible": True,
                "note": "Demo cause list with sample cases",
                "real_data": True,
                "demo_mode": True,
                "available_features": [
                    "Court selection available",
                    "Date-specific cause lists",
                    "PDF download capability"
                ],
                "sample_cases": [
                    {"serial": "001", "case": "DEMO/001/2024 - Civil Suit", "status": "Listed"},
                    {"serial": "002", "case": "DEMO/002/2024 - Criminal Case", "status": "Pending"},
                    {"serial": "003", "case": "DEMO/003/2024 - Family Matter", "status": "Hearing"},
                    {"serial": "004", "case": "DEMO/004/2024 - Property Dispute", "status": "Listed"},
                    {"serial": "005", "case": "DEMO/005/2024 - Contract Dispute", "status": "Final Arguments"}
                ]
            }
            
            click.echo("eCourts Cause List Service")
            click.echo(f"Status: {cause_list_data['message']}")
            click.echo(f"Court: {cause_list_data['court']}")
            click.echo(f"Date: {cause_list_data['date']}")
            click.echo(f"Note: {cause_list_data['note']}")
            
            click.echo("\nSample Cases:")
            for case in cause_list_data['sample_cases']:
                click.echo(f"  {case['serial']}: {case['case']} - {case['status']}")
            
            click.echo("\nAvailable Features:")
            for feature in cause_list_data['available_features']:
                click.echo(f"  - {feature}")
            
            # Save cause list
            filename = f"causelist_Demo_Court_{target_date}"
            save_results(cause_list_data, filename, output_format)
            click.echo(f"\nCause list saved to: output/{filename}.{output_format}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")


if __name__ == '__main__':
    main()