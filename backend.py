from linkedin_scraper import *
from data_handler import *
import tkinter.messagebox as messagebox


def close_script(driver, script_window=None):
    driver.quit()
    if script_window:
        script_window.after(0, lambda: script_window.confirm_login.configure(state="normal"))


def main_script(username, password, delay, companies, titles, driver_path, csv_path, xlsx_path, script_window, stop_event):
    print("Companies:", companies)
    print("Titles:", titles)

    """
    Declare the path and web browser that will be used for conducting searches. 
    """
    # service = Service(r'C:\Users\AidanShinfeld\Desktop\Scripts\edgedriver_win64\msedgedriver.exe')  # Adjust path as needed
    service = Service(driver_path)
    driver = webdriver.Edge(service=service)


    driver.get("https://www.linkedin.com/feed/")
    
    #Login into Linkedin
    script_window.after(0, script_window.update_status, "Logging in!")

    login(driver, username, password)
    start_time = time.time()
    timeout = 60 

    script_window.after(0, script_window.update_status, "Confirm Login!")

    while script_window.confirm_login.get() != 1:
        if stop_event.is_set():
            messagebox.showerror("Stop Button Clicked", "Shutting Down Script!")
            close_script(driver)
            return 

        if time.time() - start_time > timeout:
            messagebox.showerror("Confirmation Needed", "Please Confirm Login!")
            timeout = timeout + 60
            if timeout > 180: 
                messagebox.showerror("Timeout for Login Confirmation","Shutting Down Script!")
                close_script(driver)
                return
        time.sleep(1)

    script_window.after(0, lambda: script_window.confirm_login.configure(state="disabled"))

    #Set up the search
    script_window.after(0, script_window.update_status, "Setting Up Search!")
    set_up_search(driver)

    total_searches = len(companies) * len(titles)
    completed_searches = 0

    
    for company in companies:
        company_info = LinkedinDirectory()
        script_window.after(0, script_window.update_status, "Running Search!")
        for title in titles:
            if stop_event.is_set():
                print("Stopping Script mid-title due to user class")
                close_script(driver, script_window)
                return

            script_window.after(0, script_window.update_search, f"{company} : {title}")
            link = None
            retries = 3
            while retries > 0 and not link:
                searchName(driver, title, company)
                name, link = getLink(driver)
                if name and link: 
                    break 
                print(f"Retrying... {retries} attempt left.")
                retries -= 1 
                time.sleep(delay)
           
            if name and link:
                person = LinkedinMember(name, title, link)
                company_info.add_member(person)
            else:
                print(f"Failed to find link for {title} at {company}. Skipping.")
            
            completed_searches += 1
            
            script_window.after(0, script_window.update_progress, completed_searches/total_searches)
            time.sleep(delay)

        if company_info:
            # Append data to csv file
            script_window.after(0, script_window.update_status, f"Appending {company} data to CSV!")
            dataToCSV(csv_path, company, company_info)
            print(f"Appended {company} data to csv.")
    
    # Convert csv file to excel 
    try:
        script_window.after(0, script_window.update_status, "CSV to EXCEL!")
        csvToExcel(csv_path, xlsx_path, titles)
        print("Successfully converted CSV to Excel with hyperlinks")
    except Exception as e:
        print(f"Failed to convert CSV to Excel: {e}")
    
    script_window.after(0, script_window.update_status, "Finished Run!")
    close_script(driver, script_window)
