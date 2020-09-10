import requests
from bs4 import BeautifulSoup
import xlsxwriter


def main():
    print('*******************')
    print('Game is on')
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('Job_description.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    # columns will be added manually

    # Write header
    worksheet.write(row, 0, 'Name')
    worksheet.write(row, 1, 'Department')
    worksheet.write(row, 2, 'Job Brief')
    worksheet.write(row, 3, 'Responsibilities')
    worksheet.write(row, 4, 'Education')
    worksheet.write(row, 5, 'Requirements')

    # increment row count
    row += 1

    root = 'https://resources.workable.com/job-descriptions/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0 Waterfox/56.2.10'}
    # Find your User-Agent here: https://www.whoishostingthis.com/tools/user-agent/
    result = requests.get(root, headers=headers)

    if result.status_code != 200:
        print('Error occurred')
        print('Webpage not available!')
        if result.status_code == 429:
            print('Too many requests sent')
            print('Please wait some time! 20 mins')

    src = result.content
    soup = BeautifulSoup(src, 'html.parser')

    section_list = soup.find_all('section',  {'class': 'section-list'})

    for section in section_list:
        department_div = section.find('div', {'class': 'col-12 margin-b-sm'})
        department = department_div.find('h5').text.strip()
        roles_list = section.find('ul')
        for role in roles_list.find_all('li'):
            role_name = role.find('a').string.strip()
            print(role_name)
            role_link = role.find('a')['href']

            result_job_description = requests.get(role_link, headers=headers)
            src_job_description = result_job_description.content
            job_description_soup = BeautifulSoup(
                src_job_description, 'html.parser')

            article_container = job_description_soup.find(
                'div', {'class': 'article-container tmpl'})

            job_brief = [0, 0]
            job_responsibilities = [0, 0]
            job_requirements = 0
            article_container_tags = article_container.find_all()
            for i, article_tag in enumerate(article_container_tags):
                if article_tag.text == 'Job brief':
                    job_brief[0] = i
                if article_tag.text == 'Responsibilities':
                    job_brief[1] = i
                    job_responsibilities[0] = i
                if article_tag.text == 'Requirements':
                    job_responsibilities[1] = i
                    job_requirements = i

            # Collect job brief data
            job_brief_tags = article_container_tags[job_brief[0]+1:job_brief[1]]
            job_brief_text_list = []
            for tag in job_brief_tags:
                if tag.text not in job_brief_text_list and tag.name == 'p':
                    job_brief_text_list.append(tag.text)

            if len(job_brief_text_list) == 0:
                print('Some of the listings have different layout')

            job_brief_text = ' '.join(job_brief_text_list)

            # collect job Responsibilities
            job_resp_start = job_responsibilities[0] + 1
            job_resp_stop = job_responsibilities[1]
            job_responsibilities_tags = article_container_tags[job_resp_start:job_resp_stop]
            job_resp_text_list = []
            for tag in job_responsibilities_tags:
                if tag.text not in job_resp_text_list and tag.name == 'li':
                    job_resp_text_list.append(tag.text)

            job_resp_text = ' '.join(job_resp_text_list)

            # collect job Requirements
            job_req_tags = article_container_tags[job_requirements:]
            job_req_text_list = []
            for tag in job_req_tags:
                if tag.text not in job_req_text_list and tag.name == 'li':
                    job_req_text_list.append(tag.text)

            job_req_text = '. '.join(job_req_text_list[:-1])

            education = job_req_text_list[-1]

            # Write data to CSV
            data = [role_name, department, job_brief_text,
                    job_resp_text, education, job_req_text, '\n']
            with open('colected_data.csv', mode='a+', encoding='utf-8') as my_file:
                text = '\t'.join(data)
                my_file.write(text)

            # Write data to XLSX
            worksheet.write(row, 0, role_name)
            worksheet.write(row, 1, department)
            worksheet.write(row, 2, job_brief_text)
            worksheet.write(row, 3, job_resp_text)
            worksheet.write(row, 4, education)
            worksheet.write(row, 5, job_req_text)
            row += 1

    workbook.close()

    print('*******************')
    print('Done!')


if __name__ == "__main__":
    main()
