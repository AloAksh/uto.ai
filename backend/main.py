from flask import Flask, request
from flask_cors import CORS
from langchain_community.llms import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.retrieval_qa.base import VectorDBQA

app = Flask(__name__)
CORS(app, origins="*")  # Allow requests from any origin

information = """
https://www.legalserviceindia.com/legal/article-7334-rights-of-under-trial-prisoners-in-india.html,
https://lddashboard.legislative.gov.in/sites/default/files/COI...pdf,
https://nhrc.nic.in/sites/default/files/11%20Rights%20of%20Prisoners-compressed.pdf,
https://www.livelaw.in/news-updates/issues-undertrials-standing-stubborn-against-face-democracy-rajasthan-hc-grants-bail-ndpsaccused-jail-6yrs-213854,
https://www.livelaw.in/high-court/bombay-high-court/bombay-high-court-undertrials-court-physically-cumbersome-vc-facility-presence-243535,
https://nyaaya.org/nyaaya-weekly/what-are-the-rights-of-undertrial-prisoners/,
https://www.epw.in/journal/2016/4/commentary/undertrial-prisoners-india.html,
https://www.indiaspend.com/police-judicial-reforms/indian-prisons-saw-a-surge-in-undertrial-prisoners-over-a-decade-887939,
https://www.orfonline.org/research/justice-system-in-crisis-the-case-of-india-s-undertrial-prisoners,
https://www.drishtiias.com/daily-updates/daily-news-analysis/poor-state-of-undertrials,
https://www.indiaspend.com/police-judicial-reforms/indian-prisons-saw-a-surge-in-undertrial-prisoners-over-a-decade-887939,
https://www.orfonline.org/research/justice-system-in-crisis-the-case-of-india-s-undertrial-prisoners,
https://ghclsc.gov.in/notices/Notice-31-05-2019.pdf,
https://www.legalserviceindia.com/legal/article-7972-under-trial-prisoners-and-rule-of-law.html,
https://www.ojp.gov/ncjrs/virtual-library/abstracts/under-trial-prisoners,
https://www.humanrightsinitiative.org/download/1457162682Undertrial%20Prisoners%20and%20the%20Criminal%20Justice%20System.pdf,
https://pib.gov.in/PressReleaseIframePage.aspx?PRID=2003162,
https://frontline.thehindu.com/social-issues/indian-jails-are-overcrowded-with-pretrial-and-undertrial-prisoners-from-poor-and-marginalised-communities/article66234747.ece,
https://www.jetir.org/papers/JETIREV06030.pdf,
https://www.icle.in/wp-content/uploads/2022/09/Undertrial-prisoners-research.pdf,
https://sansad.in/getFile/loksabhaquestions/annex/1712/AU2006.pdf?source=pqals,
https://www.livelaw.in/articles/confinement-to-a-cage-the-bridled-under-trial-prisoners-in-india-254046,
https://thewire.in/rights/indian-jails-undertrial-prisoners,
https://devgan.in/crpc/section/436A/,
https://www.legalserviceindia.com/legal/article-4537-the-human-right-of-under-trail-prisoners.html,
https://indiankanoon.org/search/?formInput=under%20trial%20prisoners
"""

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(information)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(texts, embeddings)
qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=vectorstore)

@app.route("/", methods=['POST', 'OPTIONS'])
def main():
    try:
        response_headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        if request.method == 'OPTIONS':
            # Respond to OPTIONS preflight request
            response = app.make_default_options_response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'POST'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

        data = request.get_json()  # Assuming JSON input
        query = data.get('text')  # Extracting 'text' from JSON payload
        #print("Question: ===", query)
        answer = qa.run(query)
        #print("answer: ", answer)
        response_headers['Access-Control-Allow-Origin'] = "*"
        return {"response": answer}, 200, response_headers  # Returning response with headers
    except Exception as e:
        #print("ERROR:  == ", str(e))
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
