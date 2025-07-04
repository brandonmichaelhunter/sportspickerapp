Creating a Free Azure SQL Database with Naming Conventions
This guide walks developers through creating a free Azure SQL Database using the Azure portal, tailored for first-time setup. It includes a specific naming convention for the SQL Server: <state_abbrv><apptype><number>. For example, a server for a web application in California might be named CAWeb01. This document is formatted for easy copying into a README file.
Prerequisites

A Microsoft Azure account with a free trial or free credits. Sign up at azure.microsoft.com/free to get $200 in credits for 30 days or 12 months of select free services.
Basic familiarity with the Azure portal.
A public IP address for firewall configuration (use a tool like whatismyipaddress.com to find yours).

Step-by-Step Instructions
1. Sign in to the Azure Portal

Navigate to portal.azure.com and log in with your Azure credentials.
If you don’t have an account, create one to access the free tier, which includes a 250 GB Azure SQL Database at the Standard S0 tier.

2. Navigate to Azure SQL Database

In the Azure portal, click Create a resource in the left-hand navigation pane.
Under Databases, select SQL Database. This opens the Create SQL Database form.

3. Configure Project Details

Subscription: Select your free trial Azure subscription (e.g., "Azure subscription 1").
Resource Group:
Choose an existing resource group or click Create new.
Name the resource group, e.g., SQL-RG-<yourappname>. A resource group is a logical container for related Azure resources.
Example: SQL-RG-MyApp.



4. Configure Database Details

Database Name: Enter a unique name for your database, avoiding special characters or reserved keywords (e.g., "Azure"). Example: MyAppDB.
Server:
Click Create new to set up a new Azure SQL logical server.
Server Name: Follow the naming convention <state_abbrv><apptype><number>. For example:
State Abbreviation: Use a two-letter code (e.g., CA for California, NY for New York).
App Type: Use a short descriptor like Web, API, or DB to indicate the application type.
Number: Use a two-digit number (e.g., 01, 02) to differentiate instances.
Example: CAWeb01 for a web app server in California.
Note: Server names must be globally unique across Azure, so you may need to adjust the number (e.g., CAWeb02) if the name is taken.


Location: Select a region close to you or your users (e.g., East US).
Authentication Method: Choose Use SQL authentication for simplicity.
Server Admin Login: Enter a username, e.g., azureuser.
Password: Create a strong password meeting Azure’s complexity requirements (e.g., Pa$$w0rd123!) and confirm it.



5. Configure Compute + Storage

Click Configure database under Compute + storage.
For the free tier, select the Standard service tier.
Set DTUs to 10 and Data max size to 250 GB to stay within the free tier limits.
Click Apply.

6. Configure Networking

On the Networking tab, set Connectivity method to Public endpoint.
Under Firewall rules, click Add client IP to automatically add your public IP address, allowing access to the database from your machine.
Optionally, enable Allow Azure services and resources to access this server for broader access within Azure.
Click Next: Security.

7. Configure Security and Additional Settings

Security: Leave defaults (e.g., disable Microsoft Defender for SQL to avoid costs).
Additional Settings:
Under Data source, select Sample to create an AdventureWorksLT sample database with tables for testing, or choose Blank database for an empty database.
Leave other settings (e.g., collation, maintenance window) as default.


Click Next: Review + create.

8. Review and Create

On the Review + create tab, verify the Cost summary shows $0.00 USD, confirming the free tier.
Check that the server name follows the <state_abbrv><apptype><number> convention (e.g., CAWeb01).
Click Create to deploy the database. Deployment takes a few minutes.
Once complete, click Go to resource to view your new Azure SQL Database.

9. Connect to Your Database

Navigate to your database in the Azure portal (e.g., MyAppDB).
Click Query editor (preview) in the left-hand menu.
Log in with the server admin credentials (e.g., azureuser and your password).
If the sample database was selected, you’ll see tables like SalesLT.Customer. Run a query like:SELECT TOP 100 * FROM SalesLT.Customer;


For external access (e.g., via SQL Server Management Studio or DataGrip):
Ensure your client IP is added to the server’s firewall rules (see Step 6).
Use the server name (e.g., CAWeb01.database.windows.net) and your admin credentials.



Naming Convention Details
The <state_abbrv><apptype><number> convention ensures clarity and organization:

State Abbreviation: Use standard two-letter codes (e.g., CA, TX, NY). See USPS state abbreviations for a full list.
App Type: Short, descriptive terms (e.g., Web, API, DB) to indicate the application’s purpose.
Number: A two-digit identifier (e.g., 01, 02) to handle multiple instances and ensure global uniqueness.
Example: TXAPI01 for an API server in Texas, first instance.
Why Use This Convention?
Improves readability and searchability in the Azure portal.
Avoids naming collisions, as server names are globally unique.
Aligns with organizational needs for identifying resources by location and purpose.



Best Practices for First-Time Developers

Keep Names Short: Azure SQL Server names have a 63-character limit. The <state_abbrv><apptype><number> format helps stay concise.
Document Naming: Share the naming convention with your team to ensure consistency.
Use Tags: Add tags (e.g., env:dev, app:MyApp) to provide additional metadata for filtering and cost management.
Firewall Management: Regularly update firewall rules if your IP changes, or use a range for flexibility.
Free Tier Limits: The free 250 GB database is ideal for development or proof-of-concept but not recommended for production workloads. Stay within the Standard S0 tier (10 DTUs, 250 GB) to avoid charges.
Automate with Azure Policy: Use Azure Policy to enforce the naming convention across your resources.

Troubleshooting

Server Name Taken: If your server name (e.g., CAWeb01) is not unique, try incrementing the number (e.g., CAWeb02) or adding a random string (e.g., CAWeb01xyz).
Connection Issues: Verify your IP is in the firewall rules. Check the server name format (<servername>.database.windows.net) and credentials.
Costs Incurred: Ensure you selected the Standard S0 tier with 10 DTUs and 250 GB. Check your subscription’s cost summary in the Azure portal.

Additional Resources

Azure SQL Database Documentation
Azure Naming Tool for generating consistent names
Naming Rules and Restrictions for Azure Resources
Create a Free Azure Account


This free Azure SQL Database setup is perfect for developers testing applications or learning database management. By following the <state_abbrv><apptype><number> naming convention, you ensure your resources are organized and easily identifiable.
