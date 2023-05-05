import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from statsmodels.tsa.stattools import adfuller
from IPython.display import Image
from PIL import Image as Im

def synthesize_names(card):
    """_summary_

    Args:
        card (pd.DataFrame.apply):
            Used to apply on cards to replace their
            own self-referenced names with CARDNAME.
            Use axis=1.

    Returns:
        str:
            Filtered oracle texts with CARDNAME in them
    """    
    return card['oracle_text'].replace(card['name'],'CARDNAME').split('\n')

def card_sampler(
    card_data,n_cards=5,card_list=None,
    **kwargs
):
    """_summary_

    Args:
        card_data (DataFrame, required):
            A Pandas DataFrame with standardized card
            data, having keys 'index','id','name',
            'prices' and 'prices_normal' and/or
            'prices_foil'
        n_cards (int, optional): 
            Number of cards to sample form card_data.
            This is ignored if card_list is defined.
            Defaults to 5.
        card_list (list-like, optional):
            List of cards to look for by name. This
            will search card_data['name'] for any
            (lowercase) matches. Uses all matches by
            default. If this is None, instead it uses
            n_cards to define a random sample of cards
            in the provided data. Defaults to None.

    Returns:
        list:
            List of scryfall image uris for use with
            Image()
    """    
    if card_list==None:
        sample_cards = card_data.sample(n_cards).reset_index()
    else:
        sample_cards = card_data[
            card_data['name'].str.lower().isin(card_list)
            ].sort_values('name').reset_index()
    return sample_cards

def plot_card_trends(
    card_data,n_cards=5,card_list=None,
    ax=None,ax_width=14,ax_scale=3,
    **kwargs
):
    """_summary_

    Args:
        card_data (DataFrame, required):
            A Pandas DataFrame with standardized card
            data, having keys 'index','id','name',
            'prices' and 'prices_normal' and/or
            'prices_foil'
        n_cards (int, optional): 
            Number of cards to sample form card_data.
            This is ignored if card_list is defined.
            Defaults to 5.
        card_list (list-like, optional):
            List of cards to look for by name. This
            will search card_data['name'] for any
            (lowercase) matches. Uses all matches by
            default. If this is None, instead it uses
            n_cards to define a random sample of cards
            in the provided data. Defaults to None.
        ax (matplotlib.pyplot axes, optional):
            pyplot axis for the graph to be plotted
            onto. Defaults to None.
        ax_width (float, optional):
            Width of the overall pyplot figure.
            Defaults to 14.
        ax_scale (float, optional):
            Height of graphs for output. Is multiplied
            by the number of cards. Defaults to 3.
    """
    
    test_cards = card_sampler(
        card_data=card_data,
        n_cards=n_cards,
        card_list=card_list,
        **kwargs
    )
    if card_list != None:
        n_cards = len(test_cards)

    fig, ax = plt.subplots(n_cards,2,
                    figsize=(ax_width,(n_cards*ax_scale)+1),
                    sharex=True)
                    
    fuller_vals = {}

    for i, test_card in test_cards.iterrows():
        fuller_vals[test_card['id']] = {
            'name': test_card['name']
        }
        for j, style in enumerate(['normal','foil']):
            printing = f'prices_{style}'
            if n_cards == 1:
                ax_ = ax
            else:
                ax_ = ax[i]
            
            if test_card[printing] != None:
                    
                price_series = pd.Series(
                    test_card[printing].values(),
                    index = pd.DatetimeIndex(test_card[printing].keys())
                )
                x = price_series.index
                y = price_series.values
                y1 = np.diff(y)+y[0]

                fuller_vals[test_card['id']][style] = {
                        'adfuller':adfuller(y1)[1:],
                        'prices':y
                }
                
                ax_[j].plot(x,y,label='Actual Price')
                ax_[j].plot(x[1:],y1,label='Price Change')
                
                title=f"""{
                    test_card['name']
                } ({
                    test_card['set'].upper()
                }) - [{
                    test_card['index']
                }]"""
                ax_[j].set(
                    title=title
                )
                ax_[j].set_ylim(
                    bottom=(min([y.min(),y1.min()])-0.03)*0.95,
                    top=(max([y.max(),y1.max()])+0.03)*1.05
                    )
                ax_[j].legend()
                ax_[j].yaxis.set_major_formatter('${x:.2f}')
            else:
                ax_[j].set_yticks([0,0])

    if n_cards == 1:
        ax_ = [ax]
    else:
        ax_ = ax
    ax_[0][0].set(
        title=f"Non-Foil\n{ax_[0][0].get_title()}"
    )
    ax_[0][1].set(
        title=f"Foil\n{ax_[0][1].get_title()}"
    )
    for label in ax_[-1][0].get_xticklabels():
        label.set(rotation=30)
    for label in ax_[-1][1].get_xticklabels():
        label.set(rotation=30)
    plt.suptitle("Selection of Foil and Non-Foil Cards\nand Price Trends (USD)")
    plt.tight_layout()
    return fuller_vals

def card_imager(
    card_data,n_cards=5,card_list=None,
    print_out=True,img_size='normal',
    width=None,height=None,hplot=True,
    **kwargs
):
    """_summary_

    Args:
        card_data (DataFrame, required):
            A Pandas DataFrame with standardized card
            data, having keys 'index','id','name',
            'prices' and 'prices_normal' and/or
            'prices_foil'
        n_cards (int, optional): 
            Number of cards to sample form card_data.
            This is ignored if card_list is defined.
            Defaults to 5.
        card_list (list-like, optional):
            List of cards to look for by name. This
            will search card_data['name'] for any
            (lowercase) matches. Uses all matches by
            default. If this is None, instead it uses
            n_cards to define a random sample of cards
            in the provided data. Defaults to None.
        print_out (bool, optional): 
            Whether or not to display the uris in-line.
            Defaults to None.
        width, height (float, optional):
            width and height values to pass on to
            Image. None uses the returned uri's default
            values. Defaults to None.
        img_size (str,optional):
            A scryfall image uri standard size string.
            Values are: 'small', 'normal', 'large',
            'png', 'art_crop', and 'border_crop'.
            Defaults to 'normal'.

    Returns:
        list:
            List of scryfall image uris for use with
            Image()
    """    
    sample_cards = card_sampler(
    card_data,n_cards=n_cards,card_list=card_list,
    **kwargs
    )
    card_images = [card['image_uris']['normal'].split('?')[0] for i, card in sample_cards.iterrows()]
    if (print_out & ~hplot):
        for uri in card_images:
            display(Image(uri,width=width,height=height))
    # horizontal image plotting from StackOverflow:
    # https://stackoverflow.com/questions/36006136/how-to-display-images-in-a-row-with-ipython-display 
    elif(print_out & hplot):
        fig,ax = plt.subplots(
            1,len(card_images),
            figsize=(12,len(card_images)*4)
            )
        for i, uri in enumerate(card_images):
            im_buffer = Image(uri,
                width=width,height=height
                ).data
            np_buffer = np.frombuffer(im_buffer,dtype='byte')
            bgr = cv2.imdecode(np_buffer,-1)
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            ax[i].imshow(rgb)
            ax[i].axis('off')
            #Image(uri).data)
        plt.tight_layout()
    return card_images

import cv2
# import numpy as np

# f = open('image.jpg', 'rb')
# image_bytes = f.read()  # b'\xff\xd8\xff\xe0\x00\x10...'

# decoded = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)

# print('OpenCV:\n', decoded)

# # your Pillow code
# import io
# from PIL import Image
# image = np.array(Image.open(io.BytesIO(image_bytes))) 
# print('PIL:\n', image)