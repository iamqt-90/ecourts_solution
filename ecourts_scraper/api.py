"""
Optional web API interface for eCourts Scraper.
"""

from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
from .scraper import ECourtsScraper
from .utils import format_date, validate_cnr, validate_case_details


app = Flask(__name__,
            static_folder='static',
            static_url_path='/static')
scraper = ECourtsScraper()


@app.route('/', methods=['GET'])
def index():
    """Web interface for eCourts Scraper."""
    return render_template('index.html')


@app.route('/api', methods=['GET'])
def api_docs():
    """API documentation endpoint."""
    return jsonify({
        "message": "eCourts Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "search_by_cnr": "POST /search/cnr",
            "search_by_case": "POST /search/case", 
            "cause_list": "GET /causelist/<court_name>/<date>"
        },
        "example_usage": {
            "cnr_search": {
                "url": "/search/cnr",
                "method": "POST",
                "body": {"cnr": "DLCT01-123456-2023", "date": "today"}
            },
            "case_search": {
                "url": "/search/case", 
                "method": "POST",
                "body": {"case_type": "CRL", "case_number": "12345", "case_year": "2023", "date": "today"}
            }
        }
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route('/search/cnr', methods=['POST'])
def search_by_cnr():
    """Search case by CNR number."""
    try:
        data = request.get_json()
        cnr = data.get('cnr')
        date_option = data.get('date', 'today')
        captcha_code = data.get('captcha_code')  # Optional captcha code
        
        if not cnr:
            return jsonify({"error": "CNR is required"}), 400
        
        if not validate_cnr(cnr):
            return jsonify({"error": "Invalid CNR format"}), 400
        
        # Determine target date
        if date_option == 'tomorrow':
            target_date = format_date(datetime.now() + timedelta(days=1))
        else:
            target_date = format_date(datetime.now())
        
        # Demo mode for testing
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
                "demo_mode": True,
                "new_scraper": True
            }
            
            # Save to output folder
            from .utils import save_results
            filename = f"case_result_{cnr}_{target_date}"
            save_results(demo_result, filename, "json")
            
            return jsonify({
                "success": True,
                "data": demo_result,
                "search_params": {"cnr": cnr, "date": target_date},
                "demo_data": True,
                "saved_to_file": f"{filename}.json"
            })
        
        # Perform search with optional captcha
        result = scraper.search_by_cnr(cnr, target_date, captcha_code)
        
        if result.get('status') == 'error':
            return jsonify(result), 500
        
        # If captcha is required, return the captcha info
        if result.get('status') == 'captcha_required':
            return jsonify({
                "success": True,
                "captcha_required": True,
                "data": result,
                "search_params": {"cnr": cnr, "date": target_date}
            })
        
        # If we have search results, return them directly
        if result.get('status') in ['case_found', 'no_case_data', 'search_failed']:
            # Save results to output folder
            from .utils import save_results
            filename = f"case_result_{cnr}_{target_date}"
            save_results(result, filename, "json")
            
            return jsonify({
                "success": True,
                "data": result,
                "search_params": {"cnr": cnr, "date": target_date},
                "real_case_data": True,
                "saved_to_file": f"{filename}.json"
            })
        
        # Fallback to case listing
        listing = scraper.get_case_listing(result, target_date)
        
        # Save results to output folder
        from .utils import save_results
        filename = f"case_result_{cnr}_{target_date}"
        save_results(listing, filename, "json")
        
        return jsonify({
            "success": True,
            "data": listing,
            "search_params": {"cnr": cnr, "date": target_date},
            "real_ecourts_data": True,
            "saved_to_file": f"{filename}.json"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/search/case', methods=['POST'])
def search_by_case_details():
    """Search case by case type, number, and year."""
    try:
        data = request.get_json()
        case_type = data.get('case_type')
        case_number = data.get('case_number')
        case_year = data.get('case_year')
        date_option = data.get('date', 'today')
        
        if not validate_case_details(case_type, case_number, case_year):
            return jsonify({"error": "Invalid case details"}), 400
        
        # Determine target date
        if date_option == 'tomorrow':
            target_date = format_date(datetime.now() + timedelta(days=1))
        else:
            target_date = format_date(datetime.now())
        
        # Perform search
        result = scraper.search_by_case_details(
            case_type, case_number, case_year, target_date
        )
        
        if result.get('status') == 'error':
            return jsonify(result), 500
        
        # Get case listing with real eCourts data
        listing = scraper.get_case_listing(result, target_date)
        
        # Return the real eCourts data directly
        return jsonify({
            "success": True,
            "data": listing,
            "search_params": {
                "case_type": case_type,
                "case_number": case_number,
                "case_year": case_year,
                "date": target_date
            },
            "real_ecourts_data": True
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/causelist/<court_name>/<date>', methods=['GET'])
def get_cause_list(court_name, date):
    """Get full cause list for a court and date."""
    try:
        # Demo mode for cause list
        if court_name.lower() == 'demo' or 'demo' in court_name.lower():
            cause_list_data = {
                "status": "connected",
                "court": "Demo District Court",
                "date": date,
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
            
            # Save to output folder
            from .utils import save_results
            filename = f"causelist_{court_name.replace(' ', '_')}_{date}"
            save_results(cause_list_data, filename, "json")
            
            return jsonify({
                "success": True,
                "data": cause_list_data,
                "saved_to_file": f"{filename}.json"
            })
        
        cause_list = scraper.download_cause_list(court_name, date)
        
        if cause_list.get('status') == 'error':
            return jsonify(cause_list), 500
        
        return jsonify({
            "success": True,
            "data": cause_list
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)