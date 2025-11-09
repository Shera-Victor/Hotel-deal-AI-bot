from fetch_data import run_fetch
from analyze_data import run_analysis
from generate_report import generate_pdf
from send_notifications import send_email

def main():
    print("🔹 Fetching hotel data...")
    run_fetch()
    print("🔹 Analyzing trends with Prophet...")
    deals = run_analysis()
    print(f"✅ Found {len(deals)} great deals!")
    print("🔹 Generating PDF report...")
    pdf_path = generate_pdf(deals)
    print("🔹 Sending email report...")
    send_email(pdf_path)
    print("🎉 Workflow complete!")

if __name__ == "__main__":
    main()
