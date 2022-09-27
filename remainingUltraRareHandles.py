from concurrent.futures import ThreadPoolExecutor, as_completed
from blockfrost import ApiError, ApiUrls, BlockFrostApi

#BlockFrost API which allows for querying the Cardano blockchain
api = BlockFrostApi(
    project_id='mainnetJZdBd2lCOXfHSI9ENhubJYAZ5ThYpXao',
    base_url=ApiUrls.mainnet.value,
)

#Official Ada Handle policy ID
HANDLE_POLICY_ID =  "f0ff48bbb7bbe9d59a40f1ce90e9e9d0ff5002ec48f232b49ca0fb9a"

def handle_request( handle ):

    try:
        handle_encoded = handle.encode( 'utf-8' )
        handle_hex = handle_encoded.hex()
        api.asset_addresses( HANDLE_POLICY_ID + handle_hex, return_type='json' )
        print(f"{handle} is already minted")

    except ApiError:
        available_handle = handle
        print(f"{handle} is available")
        return available_handle

def get_remaining_handles():

    remaining = []
    threads= []
    #All valid characters are "abcdefghijklmnopqrstuvwxyz1234567890-_." Modify the variable below to check what interests you
    possible_characters = "abcdefghijklmnopqrstuvwxyz"
    possible_handles = []

    for c in possible_characters:
        for c2 in possible_characters:
            possible_handles.append( c + c2 )

    with ThreadPoolExecutor() as executor:
        for h in possible_handles:
            threads.append( executor.submit( handle_request, h ) )

        for task in as_completed( threads ):
            handle = task.result()
            remaining.append( handle )

    remaining_filtered = list( filter( None, remaining ) )

    return remaining_filtered

def run():

    remaining_handles = get_remaining_handles()
    remaining_amount = len( remaining_handles )
    with open("remaining.txt", "w") as file:
        for h in remaining_handles:
            file.write(f"{h}\n")
    print(f"{remaining_amount} unminted 2 Character Handles remaining")

if __name__ == '__main__':
    run()
