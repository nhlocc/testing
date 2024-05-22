import chromadb
from chromadb.utils import embedding_functions

def LoadVectorDB(
    DBpath: str = "./vectorDB/testFailEmbeddings/", 
    collectionName: str = "testfail_collecion"
):
    #CHROMA_PATH = "./tr_embeddings"
    #COLLECTION_NAME = "tr_redmine_collection"
    #COLLECTION_NAME = "testing_collecion"
    EMBEDDING_FUNC_NAME = "./models/BAAI/models--BAAI--bge-large-en-v1.5/"


    client = chromadb.PersistentClient(DBpath)

    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_FUNC_NAME,
        device='cpu'
    )

    collection = client.get_collection(
        name=collectionName, embedding_function=embedding_func
    )
    return collection

#read each row in ./data/parsed/...csv to get string
#query string = $product + $test file name + $test case description + $keyword failed + $log robot failed    => vector
#metadata = week_number
def Query(collection, question: str=" Verify The Filter function on the Resolver page of ICSCF [ims]; Keyword failed: Click Element ${Resolver_section}; Robot failed log: Element with locator 'xpath=//a[@href='/icscf/1/resolv/index']' not found.", n_results: int = 10):
    testFail = collection.query(
        query_texts=[question],
        n_results=n_results,
        include=["documents", "distances", "metadatas"],
        #where={"Module": {"$eq": module"}},
    )
    result = []
    for i in range(5):
        #result[0].append(testFail["documents"][0][i])
        result.append(testFail["metadatas"][0][i])
    print(result)
    # response_data = {
    #            "Week": "21",
    #            "Product": "SBC_CORE",
    #            "Test_File_Name": "./SBC/SILIENT_IGNORE/PCSCF/nonreg_ua.robot",
    #            "Test_case_name": "Incoming INVITE msg, From header and UA header in request msg, UA value on request message matching UA profile value",
    #            "Failed_Keyword": "Check Log HOST=AIO, PROCESS=pcscf, TYPE=list, EXPECTATION=OK, FLOW=INVITE sip,,Getting UA profile friendlyscanner from name friendlyscanner,,no matching rule, default: true,,Ignoring request silently due to peer policy",
    #            "Robot_log": "Keywords Getting UA profile friendlyscanner from name friendlyscanner is not in /tmp/VALID_auto/aio_pcscf.1",
    #            "Faiure_reason": "Product_bug"
    #       }
    return result
